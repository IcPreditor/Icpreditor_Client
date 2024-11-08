import pandas as pd
##Import comuns
import numpy as np
import pandas as pd
##Import dados processados
import sys
sys.path.insert(1, r'processing')
import processing
## Data
X_train, Y_train, X_test, Y_test,dataframe,feature_cols = processing.getInputOutput(undersampling=False,regressao=True)
dataframe = dataframe
print(dataframe.value_counts("idade"))

print(dataframe.sort)