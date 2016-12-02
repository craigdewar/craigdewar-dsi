# titanic

Requirements: Python 2.7, Anaconda with following python libraries installed (pip install dependency_name)

1. numpy
2. pandas
3. sklearn
4. csv
5. time
6. pickle

This app represents a series of pipelines. The app is made to ensure consistency in model building for a titanic dataset. The model will give likelihood of surviving the titanic, given a passengers, Pclass, Fare, Sex and AgeGroup, and there corresponding label (survived wreck or not). 

The features available in the dataset are: 

Passenger Class (categorical ordinal)
Fare: Continous real
Age: real integer
Sex: Categorical

The label (response/class) is. 

Survived: Categorical (class label) binary. 

Pipeline 1. prepare_data.sh

Creates a member of PrepareData() class and calls object method perform. Which will query a remote postgres database, and transform the data for model building purposes, and will save 2 sets of csv files. A train file set, and a test file set. Note when these files are read, they are ready for model building (no null values, category binning/dummy variable creation implemented, n - 1 dummy variables in final dataframes). 

prepare_data.sh requires four parameters that the user must enter when running the bash script, SERVER_USER, SERVER_PASSWORD, SERVER_HOST and SERVER_DB name, TEST_PERCENT, MODEL_TYPE

example, from the root directory of the app. 

sh ./prepare_data.sh server_user server_password server_host server_db table_name test_percent model_type

1. server_user = username for machine
2. server_password = password for machine
3. server_host = machine name
4. server_db = database name
5. table_name = database table name holding titanic dataset
6. test_precent = % of data to be randomly split for test data (default is 30% if no value entered)
7. model_type = Enter either logistic, or random_forest, default is integer. If random forest, all n dummys are kept in the train/test dataframes. 

The test and train csv files will be saved in ./src/main/assets. Test datasets will be saved in the test directory in assets, while train datasets will be saved in the train directory in assets. Any file will always have a unique name (by attaching timestamp to file name in Helper.generateFileName( params ). So prepare_data.sh can be run multiple times without having to delete files. 

Pipeline 2. build_model.sh

Creates a member of BuildModel() class and calls object method saveModel(). In saveModel(), the trainData set (generated from PrepareData().loadPipeline, is read as pandas dataframe, and a logistic regression model or random forest model is built (depending on model_type parameter entered when running bash file), and then saved to ./src/main/models as a series of 5 .plk files. Note all these files must be present, when importing the model in another process (In EvaluateModel().getPredictions). 

build_model.sh requires 2 parameters that the user must enter when running the bash script, FILE_NAME_TRAIN, which is the name of the csv file in assets represeting the train data set, and MODEL_TYPE. Enter logistic for MODEL_TYPE if your dataframe was split based on logistic regression prepreation, else enter random_forest, default is random_forest. 

example. from the root directory of the app/ 

sh ./build_model.sh titanic_train_07:10:16:22:32:08.csv logistic

Pipeline 3. evaluate_model.sh

Creates a member of the EvaluateModel() class, and calls the object method getPredictions. in getPredictions, the testData set (generated from PrepareData().loadPipeline), is read as a pandas dataframe, and the logistic regression model or random forest model (depending on model_type parameter entered when running bash file). Metrics outputted are model coffieicents (if logistic model), classification report, accuracy score and confusion matrix. The prediction class output is also saved with the corresponding variables in the ./assets/predictions directory (to be loaded to s3 in pipeline 4). 

evaluate_model.sh requires 3 parameters that the user must enter when running the bash script, FILE_NAME_TEST, which is the name of the csv file in assets represeting the test data set, model name (name of logit model saved during build_model.sh, and model_type. 

Note model_type should be consistent for all 3 pipelines! 

example, from the root directory of the app/ 

sh ./evaluate_model.sh titanic_test_07:10:16:22:32:08.csv titanic_model_07:10:16:22:50:21.pkl logistic

Pipeline 4. load_s3.sh

loads all files within ./src/main/assets/predictions to designed s3 bucket (aws account required, with awsCredentials (aws_access_key_id and aws_secret_access_key required). awsCredentials are entered on the command line and will be made enivironment variables throughout the process.

example, from root directory of the app/

sh ./load_s3 aws_access_key_id aws_secret_access_key aws_bucket_name

The entire pipeline is below, and should be run in this order as well. 

1. sh ./prepare_data.sh server_user server_password server_host server_db table_name test_percent model_type

2. sh ./build_model.sh train_data_set_name.csv model_type

3. sh ./evaluate_model.sh test_data_set_name.csv pipeline_model_name.pkl model_type

4. sh ./load_s3 aws_access_key_id aws_secret_access_key aws_bucket_name
