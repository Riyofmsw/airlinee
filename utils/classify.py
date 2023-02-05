import pickle
from pathlib import Path
import warnings
warnings.simplefilter("ignore")
parent_path = Path(__file__).parent
parent_path = Path(parent_path).parent
class Classify:
    def __init__(self,text) :
        self.model = f'{parent_path}/model/linear_svm.pickle'
        self.vectorizer = f'{parent_path}/model/vectorizer.pickle'
        self.text = text
    def load_model(self):
        self.loaded_model = pickle.load(open(self.model, 'rb'))
    def load_vectorizer(self):
        self.vectorizer = pickle.load(open(self.vectorizer, 'rb'))
    def map_data(self,number):
        classes=['positive','negative']
        return classes[number]
    def get_result(self):
        self.load_model()
        self.load_vectorizer()
        self.text = self.vectorizer.transform([self.text])
        result = self.loaded_model.predict(self.text)
        return self.map_data(result[0])