import os

from src.utils import download_file_from_url
from src.preprocess.preprocess import preprocess, load_and_split_data
from src.logistic_reg.logistic_reg_train import logistic_reg_train
from src.evaluation.evaluate import evaluate
from src.predict.predict import predict
import src.constants.files as files


def main(bool_dict):
    """
    Launch all project steps.

    :param bool_dict: Dictionnary with step names as keys and boolean as values allowing to bypass steps. This can be
    useful to re-run all steps but model training steps if they are already done for example.
    :return:
    """
    download_file_from_url(files.LOANS_DATA_URL, os.path.join(files.RAW_DATA, files.LOANS))

    if bool_dict["load_and_split"]:
        load_and_split_data(raw_data_path=files.LOANS,
                            training_file_path=files.TRAIN,
                            test_file_path=files.TEST)

    if bool_dict["preprocess"]:
        # TODO 1 : appeler la méthode preprocess() du module preprocess avec les arguments attendus :
        #  training_file_path, preprocessed_train_destination et preprocessing_pipeline_destination
        """
        Pour savoir quelles valeurs doivent prendre ces arguments, regarder ce que fait la méthode 
        load_and_split_data() et où elle sauvegarde les différentes données
        """
        pass

    if bool_dict["logistic_reg_train"]:
        logistic_reg_train(preprocessed_train_path="???",
                           logistic_reg_model_path="???")

    if bool_dict["predict"]:
        predict(test_file_path=files.TEST,
                preprocessing_pipeline_path=files.PREPROCESSING_PIPELINE,
                logistic_reg_model_path=files.LOGISTIC_REG_MODEL,
                prediction_file_path=files.PREDICTIONS_TEST)

    if bool_dict["evaluate"]:
        evaluate(prediction_file_path=files.PREDICTIONS_TEST)


if __name__ == "__main__":
    bool_dict = {"load_and_split": True,
                 "preprocess": True,
                 "logistic_reg_train": True,
                 "predict":True,
                 "evaluate": True
                 }
    main(bool_dict)
