from scrapper import ValorantScrapper

scr = ValorantScrapper().from_saved('./valorant_wiki')
df = scr.all_agents()
print(df.head())
