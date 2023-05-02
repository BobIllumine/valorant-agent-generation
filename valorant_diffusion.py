# !pip install diffusers
# !pip install -U transformers
# !pip install accelerate

from diffusers import StableDiffusionPipeline
import torch
import transformers
from diffusers import EulerAncestralDiscreteScheduler
import random

model_id = "ItsJayQz/Valorant_Diffusion"
pipe = StableDiffusionPipeline.from_pretrained(
    model_id,
    custom_pipeline="waifu-research-department/long-prompt-weighting-pipeline",
    torch_dtype=torch.float16
    )
pipe = pipe.to("cuda")
pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(pipe.scheduler.config)


def generateImage(my_prompt: str, out_name: str):
    prompt = "Valorant style, Character design, Illustration, KEY ART"
    prompt += my_prompt
    prompt += "Extravagent pose, Enigmatic, Confident, high dynamic range, eye catching, professional, majestic, unreal, dangerous, focused, concentrated"
    # prompt += ", Visible face, detailed face, character concept, proper anatomy, gen z, Riot Games, Disney, artstation, concept art, high contrast, full body dramatic pose, full figure, high resolution, 4K"
    # prompt += ", colorful, clean lines, pleasing angles, Attention to Detail, Comic Book Inspired Visuals, Dynamic Lighting, Technological Detailing, Expressive Animations, Distinctive Character Designs, Bold and Vibrant Colors"

    neg_prompt = "NSFW, Female, morphed, blury picture, very bright, asymmetric eyes, minimalistic, 6 fingers, ugly, dysmorphia, minor, silly, casual, low contrast, real life, naked, dull eyes, zoomed in, out of frame, multiple figures, broken fingers, bad anatomy, warped, no arms, revealing cloths, blades"
    # neg_prompt = "ugly eyes, NSFW, realistic, no arms, broken fingers, fuzzy face, ugly, cropped face, legue of legends, warped, static pose, marked edges, ((disfigured)), ((bad art)), ((deformed)),((extra limbs)),((close up)),((b&w)), blurry, (((duplicate))), ((morbid)), ((mutilated)), [out of frame], extra fingers, mutated hands, ((poorly drawn hands)), ((poorly drawn face)), (((mutation))), (((deformed))), ((ugly)), blurry, ((bad anatomy)), (((bad proportions))), ((extra limbs)), cloned face, (((disfigured))), out of frame, ugly, extra limbs, (bad anatomy), gross proportions, (malformed limbs), ((missing arms)), ((missing legs)), (((extra arms))), (((extra legs))), mutated hands, (fused fingers), (too many fingers), (((long neck))), Photoshop, ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, mutation, mutated, extra limbs, extra legs, extra arms, disfigured, deformed, cross-eye, body out of frame, blurry, bad art, bad anatomy, 3d render, nsfw, 6 fingers, background shadows, 2 face"
    # neg_prompt = "no arms, broken fingers, fuzzy face, ugly, cropped face, legue of legends, warped, swords, fantasy, static pose, marked edges, selfie, high contrast canvas frame, 3d, ((disfigured)), ((bad art)), ((deformed)),((extra limbs)),((close up)),((b&w)), wierd colors, blurry, (((duplicate))), ((morbid)), ((mutilated)), [out of frame], extra fingers, mutated hands, ((poorly drawn hands)), ((poorly drawn face)), (((mutation))), (((deformed))), ((ugly)), blurry, ((bad anatomy)), (((bad proportions))), ((extra limbs)), cloned face, (((disfigured))), out of frame, ugly, extra limbs, (bad anatomy), gross proportions, (malformed limbs), ((missing arms)), ((missing legs)), (((extra arms))), (((extra legs))), mutated hands, (fused fingers), (too many fingers), (((long neck))), Photoshop, ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, mutation, mutated, extra limbs, extra legs, extra arms, disfigured, deformed, cross-eye, body out of frame, blurry, bad art, bad anatomy, 3d render, nsfw, 6 fingers, background shadows, 2 face, cropped, revealing clothes, short clothes, fuzy face"

    image = pipe.text2img(prompt, width=1024, height=1024, negative_prompt=neg_prompt, max_embeddings_multiples=10).images[0]
    # image = pipe(prompt).images[0]

    image.save(f"./{out_name}.png")
