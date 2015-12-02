function export_edgelist(edgelist, filepath, imgsize)
    fid = fopen(filepath,'wt');
    fprintf(fid, '%.0f, %.0f\n', imgsize(1), imgsize(2));
    for i = 1:length(edgelist)
        flattened_array = reshape(edgelist{i}', [1, numel(edgelist{i})]);
        stringified_array = sprintf('%.0f,' , flattened_array);
        stringified_array = stringified_array(1:end-1);
        fprintf(fid, '%s\n', stringified_array);
%         fprintf('%s\n', stringified_array);
    end
    fclose(fid);
end
