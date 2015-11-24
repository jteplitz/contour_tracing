function connected_edgelist = extend_veins(edgelist)

    LENGTH_THRESHOLD = 30;
    PROXIMITY_MERGE_THRESHOLD = 5;
    PROXIMITY_MERGE_SLOPE_THRESHOLD = 0.1;
    
    new_edgelist = {};
    
    % Filter out segments below a certain length
    for i = 1:length(edgelist)
        if (segment_length(edgelist{i}) > LENGTH_THRESHOLD)
            new_edgelist{1,length(new_edgelist)+1} = edgelist{i};
        end
    end
    
    % Re-orient segments to be top-down
    for i = 1:length(new_edgelist)
       if(new_edgelist{i}(1,2) > new_edgelist{i}(end,2))
            new_edgelist{i} = flipud(new_edgelist{i});
       end
    end
    
    % Connect attached segments with similar slopes
    for i = 1:length(new_edgelist)
        for j = 1:length(new_edgelist)
            if (i ~= j && numel(new_edgelist{i}) > 1 && numel(new_edgelist{j}) > 1)
                i_start     = new_edgelist{i}(1,:);
                i_end       = new_edgelist{i}(end,:); 
                j_start     = new_edgelist{j}(1,:);
                j_end       = new_edgelist{j}(end,:);
                
                i_slope     = (i_end(2) - i_start(2)) / (i_end(1) - i_start(1));
                j_slope     = (j_end(2) - j_start(2)) / (j_end(1) - j_start(1));
                
                slope_diff  = abs(i_slope - j_slope);
                
                if (pdist2(i_end, j_start) < PROXIMITY_MERGE_THRESHOLD)
                    if (slope_diff < PROXIMITY_MERGE_SLOPE_THRESHOLD)
                        new_edgelist(i) = {[new_edgelist{i}; new_edgelist{j}]};
                        new_edgelist(j) = {-1};
                    end
                end 
            end
        end
    end
    
    connected_edgelist = {};
    
    for i = 1:length(new_edgelist)  
       if (numel(new_edgelist{i}) ~= 1)
            connected_edgelist{1,length(connected_edgelist)+1} = new_edgelist{i};
       end
    end
    
    edgelist = connected_edgelist;
    
    % Extend segments to find intersections

end
