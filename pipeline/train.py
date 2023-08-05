from sklearn.ensemble import GradientBoostingClassifier
import pickle
import os

class Train():
    def __init__(self, train_x, train_y):
        self.train_x = train_x
        self.train_y = train_y


    def validation(self, length_frac, model, accuracy_loc):
        train_len = int(len(self.train_x)*length_frac)
        model.fit(self.train_x[:train_len],self.train_y[:train_len])
        accuracy = model.score(self.train_x[train_len:], self.train_y[train_len:])
        if not os.path.exists(accuracy_loc):
            with open(accuracy_loc, 'w') as file:
                file.write(str(accuracy))
            return True
        with open(accuracy_loc, 'r') as file:
            saved_accuracy = float(file.read())
        if accuracy - saved_accuracy > -0.02:
            return True
        return False

    def train(self, accuracy_loc, model_location, learning_rate = 0.01, n_estimators = 500, val_frac = 0.95):
        if not os.path.exists(model_location):
            clf = GradientBoostingClassifier(random_state=0, learning_rate=learning_rate, n_estimators=n_estimators)
            _ = self.validation(val_frac,clf,accuracy_loc)
            clf.fit(self.train_x, self.train_y)
            pickle.dump(clf, open(model_location, 'wb'))
        else:
            clf = pickle.load(open(model_location, 'rb'))
            better = self.validation(val_frac,clf,accuracy_loc)
            if better:
                clf.fit(self.train_x,self.train_y)
                pickle.dump(clf, open(model_location, 'wb'))

        