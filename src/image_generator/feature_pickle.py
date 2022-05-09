import pickle

with open('../../files/features_thr_0.3.pkl', 'rb') as f:
    feat_pickle = pickle.load(f)

'''
    feat_pickle은 리스트의 리스트임
    [[이미지 이름의 리스트], [해당 이미지에서 feature], [feature의 class]]

    feat_pickle[0][0] MH105_HSCB_tallrib.png
    feat_pickle[1][0] MH105_HSCB_tallrib.png에서 얻어진 137 class의 feature
    feat_pickle[2][0] 137번 class
    
    len(feat_pickle[0]) 은 이미지의 수가 아니라 featrue의 수임
    한 이미지에 여러 feature가 나오는데 모두 따로 이미지 이름, feature, class로 저장해둠

    confidence threshold는 0.3 사용
'''
'''print(feat_pickle[0][0])
print(feat_pickle[1][0])
print(feat_pickle[2][0])'''
print(len(feat_pickle[2]))
