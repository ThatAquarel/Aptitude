import spacy

# answer = "Permettre à la colonie de se développer sans que le roi ait besoin d'investir."
# result = "Le roi ne veut pas payer pour développer sa colonie."
# result = "Régime de distribution de terres qui permet d'organiser le territoire et les relation sociales."

# answer = "Ne pas payer"
# result = "Ne pas investir"
# 97% match
# answer = "Ne pas payer"
# result = "Sans investir"
# 42% match

nlp = spacy.load('fr_core_news_lg')
tokens_answer = nlp(answer)
tokens_result = nlp(result)

print(tokens_answer.similarity(tokens_result))
