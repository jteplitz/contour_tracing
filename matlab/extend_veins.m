function edgelist = extend_veins(edgelist)

    LENGTH_THRESHOLD = 30;
    PROXIMITY_MERGE_THRESHOLD = 5;
    PROXIMITY_MERGE_SLOPE_THRESHOLD = 0.1;
    EXTENSION_STEP_SIZE = 5;
    MAX_EXTENSION = 40;
    
    new_edgelist = {};
    
    % Filter out segments below a certain length
    for i = 1:length(edgelist)
        if (segment_length(edgelist{i}) > LENGTH_THRESHOLD)
            new_edgelist{1,length(new_edgelist)+1} = edgelist{i};
        end
    end
    
    % Re-orient segments to be top-down
    for i = 1:length(new_edgelist)
       if(new_edgelist{i}(1,1) > new_edgelist{i}(end,1))
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
                
                i_slope     = atan((i_end(1) - i_start(1)) / (i_end(2) - i_start(2)));
                j_slope     = atan((j_end(1) - j_start(1)) / (j_end(2) - j_start(2)));
                
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
    extend_further = ones(1, length(new_edgelist));
    for extendIter = 1:(MAX_EXTENSION/EXTENSION_STEP_SIZE)
        for i = 1:length(edgelist)
            cur_seg = edgelist{i};
            if(extend_further(i))
                % do the extension on both sides
                if(length(cur_seg) == 2)
                    top_start       = cur_seg(1,:);
                    top_end         = cur_seg(2,:);
                    bottom_start    = top_end;
                    bottom_end      = top_start;
                else
                    top_start       = cur_seg(1,:);
                    top_end         = cur_seg(3,:);
                    bottom_start    = cur_seg(end,:);
                    bottom_end      = cur_seg(end-2,:);
                end
                top_angle = atan((top_end(1) - top_start(1)) / (top_end(2) - top_start(2)));
                bottom_angle = atan((bottom_end(1) - bottom_start(1)) / (bottom_end(2) - bottom_start(2)));
                
                disp(sprintf('%f',180*top_angle/pi));
                
                new_top_x       = top_start(2) - (cos(top_angle) * EXTENSION_STEP_SIZE);
                new_top_y       = top_start(1) + (sin(top_angle) * EXTENSION_STEP_SIZE);
                new_bottom_x    = bottom_start(2) + (cos(bottom_angle) * EXTENSION_STEP_SIZE);
                new_bottom_y    = bottom_start(1) - (sin(bottom_angle) * EXTENSION_STEP_SIZE);
                edgelist{i}     = [new_top_y, new_top_x; edgelist{i}; new_bottom_y, new_bottom_x];
                
                % if intersection is now found, do not extend on future
                % iterations
                
                for j = 1:length(edgelist)
                   if (i ~= j)
                      if (numel(polyxpoly(edgelist{i}(:,2), edgelist{i}(:,1), edgelist{j}(:,2), edgelist{j}(:,1))) ~= 0)
                          extend_further(i) = 0;
                          break;
                      end
                   end
                end
                
                
            end
        end
    end
    
end
