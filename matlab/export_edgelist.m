function export_edgelist(edgelist, filepath)
    fid = fopen(filepath,'wt');
    for i = 1:length(edgelist)
        flattened_array = reshape(edgelist{i}', [1, numel(edgelist{i})]);
        stringified_array = sprintf('%.0f,' , flattened_array);
        stringified_array = stringified_array(1:end-1);
        fprintf(fid, '%s\n', stringified_array);
    end
    fclose(fid);
end
