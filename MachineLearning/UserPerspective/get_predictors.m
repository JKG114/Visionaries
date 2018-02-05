function X = get_predictors(varargin)

X = [];
for input_num=2:2:length(varargin)
    source_data = varargin{input_num-1};
    delays = varargin{input_num};
    for dnum = 1:length(delays)
        if delays(dnum)==0
            X = [X source_data];
        else
            delayed_data = [zeros(delays(dnum),size(source_data,2));source_data(1:(end-delays(dnum)),:)];
            X = [X delayed_data];
        end
    end
end