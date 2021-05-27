import logging
import os

from monitor.monitor import monitor_loans_ratio, monitor_input_drift
from predict.predict import predict
import constants.files as files
import constants.models as m

for i in range(1, 10):
    monitor_input_drift(f"./data/interim/loans_deflation_0.{i}0.csv", "./data/output/input_stats_history.csv")

