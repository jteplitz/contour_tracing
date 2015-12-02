function new_edgelist = length_filter(edgelist, length_threshold)
% Filter out segments below a certain length
    new_edgelist = {};
    for i = 1:length(edgelist)
        if (segment_length(edgelist{i}) > length_threshold)
            new_edgelist{1,length(new_edgelist)+1} = edgelist{i};
        end
    end
end