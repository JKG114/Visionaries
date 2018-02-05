DATA_FILE = 'hourly/winter_hourly.csv';
% DATA_FILE = 'hourly/spring_hourly.csv';
% DATA_FILE = 'hourly/summer_hourly.csv';
if ~exist('data_read','var') || ~strcmp(data_read,DATA_FILE)
    disp(sprintf('Reading data from file: %s',DATA_FILE));
    [Xnum,Xstr,Xout,Xin,sttn_id,num_var_labels,str_var_labels] = read_hour_data(DATA_FILE);
    data_read = DATA_FILE;
end
sttn_out_total = sum(Xout);
sttn_in_total = sum(Xin);

[outgoing_sorted,out_rank] = sort(sttn_out_total,'descend');
[incoming_sorted,in_rank] = sort(sttn_in_total,'descend');

% STATION_ID = sttn_id
station_column = find(ismember(sttn_id,STATION_ID));

months = unique(Xnum(:,2));

%prediction_target = Xout(:,station_column);                          %predicted variable - one station
prediction_target = sum(Xout(:,station_column),2);                    %predicted variable - sum over multiple stations

%X = get_predictors(prediction_target,1);                       %predictors: outgoing value of previous hour for the same station (1 total)
%X = get_predictors(Xnum,0);                                    %predictors: common numeric variables only (6 total)
%X = get_predictors(prediction_target,1:24);                    %predictors: outgoing values of past 24 hours of same station (24 total)
X = get_predictors(Xnum(:,[1:6]),0,prediction_target,1:40);     %predictors: common numeric variables except Day and the outgoing values of past 24 hours of same station (29 total)

prediction = zeros(size(prediction_target));
for cv_index = 1:length(months)
    cv_value = months(cv_index);
    disp(sprintf('Cross validation round %d/%d: Month %d',cv_index,length(months),cv_value));
    test_data_idx = find(ismember(Xnum(:,2),cv_value));
    train_data_idx = find(~ismember(Xnum(:,2),cv_value));
% B = regress(prediction_target(train_data_idx),X(train_data_idx,:));
%  T = fitrtree(X(train_data_idx,:),prediction_target(train_data_idx),'OptimizeHyperparameters','all');
     T = fitrsvm(X(train_data_idx,:),prediction_target(train_data_idx),'Standardize',true,'epsilon',0.000000001,'HyperparameterOptimizationOptions','randomsearch');
% new_prediction = X(test_data_idx,:) * B;
    new_prediction = predict(T,X(test_data_idx,:));
    cv_score(cv_index) = mean(abs(prediction_target(test_data_idx)-new_prediction));
    prediction(test_data_idx) = new_prediction;
    disp(sprintf('Mean absolute difference for month %d: %0.2f',cv_value,cv_score(cv_index)));
end
score = mean(cv_score);
disp(sprintf('Total mean absolute difference: %0.2f',score));
OUTPUT_FILE = strrep(DATA_FILE,'.csv','_predictions.csv');
fo = fopen(OUTPUT_FILE,'w');
fprintf(fo,'month,true value,prediction\n');
for i1=1:size(prediction_target,1)
    fprintf(fo,'%d,%f,%f\n',Xnum(i1,2),prediction_target(i1),prediction(i1));
end
fclose(fo);

% To make prediction for eac station: Comment out line 15 and run the
% following line on the command window        
% for sti=1:10,STATION_ID=sttn_id(out_rank(sti));bike_out_cv;copyfile(OUTPUT_FILE,strrep(OUTPUT_FILE,'.csv',['_' num2str(STATION_ID) '.csv']));end
% To find the best station: sttn_id(out_rank(1))
