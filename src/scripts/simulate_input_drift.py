import os
import logging
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from sklearn.linear_model import LinearRegression

from predict_and_monitor import predict_and_monitor
import constants.files as files
import constants.models as m
from scripts.deflation_on_applicant_incomes import create_deflated_input_dfs
from utils import upload_pandas_df_to_s3, setup_logs, delete_s3_file, load_pandas_df_from_s3


def plot_input_stats(input_stats_history):
    matplotlib.rcParams.update({'font.size': 22})

    plt.figure(1, figsize=(25, 12))

    plt.scatter(input_stats_history["timestamp"],
                input_stats_history["mean_income"], label="mean income")

    lin_reg = LinearRegression()
    lin_reg.fit(np.array(range(m.INPUT_DRIFT_SPAN_IN_DAYS)).reshape(-1, 1),
                input_stats_history.tail(m.INPUT_DRIFT_SPAN_IN_DAYS)["mean_income"].values)

    plt.plot(input_stats_history.tail(m.INPUT_DRIFT_SPAN_IN_DAYS)["timestamp"],
             lin_reg.predict(np.array(range(m.INPUT_DRIFT_SPAN_IN_DAYS)).reshape(-1, 1)),
             label="régression linéaire", linewidth=3, color="green")

    plt.xlabel("date")
    plt.ylabel("mean income")

    plt.title("Input drift detection on mean income", fontsize=30)
    plt.legend()
    plt.savefig(os.path.join(files.LOCAL_ROOT_PATH, "data", "output", "input_drift_plot.png"))

    plt.close()


if __name__ == "__main__":
    setup_logs()
    create_deflated_input_dfs()
    delete_s3_file(files.S3_BUCKET, files.INPUT_STATS_HISTORY)
    delete_s3_file(files.S3_BUCKET, files.PREDICTIONS_HISTORY)

    logging.info("STABLE SITUATION")
    for i in range(7, 0, -1):
        new_loans = pd.read_csv(os.path.join(files.LOCAL_ROOT_PATH, "data", "interim", f"loans_deflation_0.90.csv"))
        new_loans.to_csv(files.NEW_LOANS_TO_ACCEPT.replace("/", "-"), index=False)
        upload_pandas_df_to_s3(new_loans, files.S3_BUCKET, files.NEW_LOANS_TO_ACCEPT)

        predict_and_monitor()

    logging.info("INPUT DRIFT BEGINS")
    for i in range(8, 0, -1):
        new_loans = pd.read_csv(os.path.join(files.LOCAL_ROOT_PATH, "data", "interim", f"loans_deflation_0.{i}0.csv"))
        new_loans.to_csv(files.NEW_LOANS_TO_ACCEPT.replace("/", "-"), index=False)
        upload_pandas_df_to_s3(new_loans, files.S3_BUCKET, files.NEW_LOANS_TO_ACCEPT)

        try:
            predict_and_monitor()
        except:
            logging.warning("Accepted loans ratio is too low !")
            break

    input_stats_history = load_pandas_df_from_s3(files.S3_BUCKET, files.INPUT_STATS_HISTORY)
    predictions_history = load_pandas_df_from_s3(files.S3_BUCKET, files.PREDICTIONS_HISTORY)

    plot_input_stats(input_stats_history)