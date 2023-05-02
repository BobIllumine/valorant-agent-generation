import os
from collections import defaultdict

import fandom
import nltk
from nltk import word_tokenize
import pandas as pd
import shutil
import re


class ValorantScrapper:
    """
    Class for data extraction from fandom wiki
    """
    agents_list = ['Astra', 'Breach', 'Brimstone', 'Chamber',
                   'Cypher', 'Fade', 'Gekko', 'Harbor', 'Jett',
                   'KAYO', 'Killjoy', 'Neon', 'Omen', 'Phoenix',
                   'Raze', 'Reyna', 'Sage', 'Skye',
                   'Sova', 'Viper', 'Yoru']

    def __init__(self, output_dir: str = './valorant_wiki', persist: bool = True):
        """
        Class constructor
        :param output_dir: Output directory. `./valorant_wiki` by default
        :param persist: Flag to determine whether files should persist after the execution. `True` by default
        """
        self.out_dir = os.path.join(output_dir)
        self.persist = persist
        self.agents_dict = defaultdict().fromkeys(ValorantScrapper.agents_list)
        os.makedirs(self.out_dir, exist_ok=True)
        fandom.set_wiki('valorant')
        fandom.set_rate_limiting(rate_limit=False)

    def __getitem__(self, item: str) -> tuple[pd.DataFrame, str] | None:
        if self.agents_dict.get(item) is None:
            try:
                self.agents_dict[item] = self.__agent_page(item)
            except AssertionError:
                return None
        return self.agents_dict[item]

    def __agent_page(self, name: str) -> tuple[pd.DataFrame, str]:
        """
        Retrieve an agent page
        :param name: Agent's name
        :param save: Flag to determine whether to save the file or not
        :return: tuple[pd.DataFrame, str] -- prepared DataFrame and raw text
        """
        assert name in ValorantScrapper.agents_list
        page = fandom.page(name)
        needed_sections = ['Biography', 'Personality', 'Appearance', 'Abilities', 'Relations']
        raw_text = name
        raw_list = []
        for sec in needed_sections:
            if page.section(sec) is None or len(page.section(sec)) == 0:
                continue
            raw_text += f'\n\n{sec}\n'
            # Get rid of all links
            first_cleanup = re.sub(
                r'(https?:\/\/(?:www\.|(?!www)))[-a-zA-Z0-9@:%._\+~#=]{1,256}\.'
                r'[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)',
                '', page.section(sec))
            lines = first_cleanup.splitlines()
            if sec == 'Biography':
                # First 4 lines are unnecessary
                lines = lines[4:]
                first_cleanup = '\n'.join(lines)
                # Get rid of `Timeline of Events` part (since it is poorly structured)
                first_cleanup = re.sub(r'[^\n]*Early Life.*', '', first_cleanup, flags=re.DOTALL)
            # Get rid of all references
            second_cleanup = re.sub(r'\[.+\]', '', first_cleanup)
            third_cleanup = second_cleanup.removeprefix(f'{sec}\n')
            raw_text += third_cleanup
            raw_list.append([name, sec, third_cleanup, len(word_tokenize(third_cleanup))])

        df = pd.DataFrame(raw_list, columns=['title', 'heading', 'content', 'tokens'])
        df = df.set_index(['title', 'heading'])
        if self.persist:
            os.makedirs(os.path.join(self.out_dir, 'agents', name), exist_ok=True)
            df.to_csv(
                os.path.join(self.out_dir, 'agents', name, f'{name}.csv'),
                header=True,
                index=True
            )
            with open(os.path.join(self.out_dir, 'agents', name, f'{name}.txt'), 'w') as f:
                f.write(raw_text)

        return df, raw_text

    def all_agents(self, out_name: str = 'all') -> pd.DataFrame:
        dfs = []
        for agent in ValorantScrapper.agents_list:
            dfs.append(self[agent][0])
        agents = pd.concat(dfs, axis=0)
        agents = agents.set_index(['title', 'heading'])
        if self.persist:
            agents.to_csv(
                os.path.join(self.out_dir, 'agents', f'{out_name}.csv'),
                index=True, header=True
            )
        return agents

    @staticmethod
    def from_saved(path: str):
        scrapper = ValorantScrapper(path)
        for file in os.listdir(os.path.join(path, 'agents')):
            if os.path.isdir(os.path.join(path, 'agents', file)):
                with open(os.path.join(path, 'agents', file, f'{file}.txt')) as f:
                    scrapper.agents_dict[file] = [pd.read_csv(os.path.join(path, 'agents', file, f'{file}.csv')), f.read()]
        return scrapper

    def __del__(self):
        if not self.persist and os.path.exists(self.out_dir):
            shutil.rmtree(self.out_dir, ignore_errors=True)
