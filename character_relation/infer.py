from tensorflow import keras

from character_relation.model import CharacterRelationModel
from character_relation.config import LANGUAGE

model = CharacterRelationModel()

keras_model = keras.models.load_model(f"character_relation_model_{LANGUAGE}")

# test_sentences = [
#     "My boss at work is extremely toxic, he insults everyone.",
#     "He's my accomplice.",
#     "He's my rival in a swimming competition",
#     "Romeo and Juliet, the two secret lovers of the Shakespeare era.",
#     "The love and hate relationship that I have with her.",
#     "My coworker and I work very efficiently together.",
#     "He's so boring and always has a serious tone.",
#     "A social media influencer has many attracted and dedicated fans.",
#     "They kissed in front of everyone at a party."
# ]
test_sentences = [
    "张无忌此时已然明白，原来赵敏将各派高手囚禁此处，使药物抑住各人的内力，逼迫他们投降朝廷。",
    "赵敏喜道：“当真么？”",
    "张无忌道：“周姑娘和我……也没甚么……只是……只是……”说了两个“只是”，却接不下去。",
    "赵敏笑道：“张公子，这般花容月貌的人儿，我见犹怜。",
    "张无忌想起宋大伯、俞二伯等身在敌手，赵敏对何太冲、唐文亮等又如此折辱，不由得忧心如焚",
    "赵敏轻轻的道：“无忌哥哥，我和你初次相遇绿柳山庄，后来一起跌入地牢，这情景不跟今天差不多么？”",
    "赵敏向张无忌横了一眼，抿嘴笑道：“日后教主要去波斯，去会见一位要紧人物，那时你可随同前去，向他们的高手匠人请教。",
    "赵敏听他说得诚恳，倚在他的怀里。",
    "赵敏轻轻的道：“无忌哥哥，我和你初次相遇绿柳山庄，后来一起跌入地牢，这情景不跟今天差不多么？”"
    "张无忌嗤的一声笑，伸手抓住她左脚，脱下了她鞋子。",
    "赵敏玉颊晕红，低下了头，道：“你传授范右使这几招武功，只让他震断宋青书的手臂，何以不教他取了那姓宋的性命？”",
    "赵敏也正望着他，二人目光相触，赵敏眼色中似笑非笑，嘴角微斜，似有轻蔑之意，也不知是嘲笑张无忌狼狈失措，还是瞧不起峨嵋派虚张声势"
]
y = keras_model.predict(model.preprocess(test_sentences))
print(y)
