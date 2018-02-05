function [Xnum,Xstr,Xout,Xin,station_id,num_var_labels,str_var_labels] = read_hour_data(filename)

fi = fopen(filename,'r');

Xnum = [];
Xstr = {};
Xout = [];
Xin = [];
nc = 0;
while 1
    input_line = fgetl(fi);
    if ~ischar(input_line), break, end
    entries=strsplit(input_line,',');
    nc=nc+1;
    if nc == 1
        labels = entries;
        num_var_labels = labels([1 2 4 5 7 8]);
        str_var_labels = labels([3 6]);
        continue;
    end
    Xnum(nc-1,1:6) = str2num(char(entries([1 2 4 5 7 8])))';
    Xstr(nc-1,1:2) = entries([3 6]);
    outgoing_new = str2num(char(entries(10:3:end)))';
    incoming_new = str2num(char(entries(11:3:end)))';
    Xout(nc-1,1:length(outgoing_new)) = outgoing_new;
    Xin(nc-1,1:length(incoming_new)) = incoming_new;
end
station_id = str2num(char(entries(9:3:end)))';

fclose(fi);