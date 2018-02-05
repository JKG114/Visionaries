function y = one_hot(x)
n = size(x,1);
y = [];
for col=1:size(x,2)
    categories = unique(x(:,col));
    new_variables = zeros(n,length(categories));
    for c=1:length(categories)
        new_variables(:,c) = ismember(x(:,col),categories(c));
    end
    y = [y new_variables];
end