# import openai
# from flask import request, jsonify



# def generate_text():
#     prompt = request.json['prompt']
#     response = openai.Completion.create(
#         engine="davinci",
#         prompt=prompt,
#         max_tokens=60,
#         n=1,
#         stop=None,
#         temperature=0.5,
#     )
#     return jsonify({'text': response.choices[0].text})