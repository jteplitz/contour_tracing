function edgelist = extend_veins(edgelist)

    LENGTH_THRESHOLD = 30;
    PROXIMITY_MERGE_THRESHOLD = 5;
    PROXIMITY_MERGE_SLOPE_THRESHOLD = 0.1;
    EXTENSION_STEP_SIZE = 10;
    MAX_EXTENSION = 100;
    
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
    
    % Remove edges who were eliminated in the previous step, forming a new
    % clean edgelist of connected edges
    for i = 1:length(new_edgelist)  
       if (numel(new_edgelist{i}) ~= 1)
            connected_edgelist{1,length(connected_edgelist)+1} = new_edgelist{i};
       end
    end
    
    edgelist = connected_edgelist;
    
    %% Extend segments to find intersections
    
    % Compute all top and bottom angles
    top_deltas = zeros(2, length(edgelist));
    bottom_deltas = zeros(2, length(edgelist));
    
    for i = 1:length(edgelist)
        cur_seg = edgelist{i};
        
        % start points are the top and bottom endpoints of the edge, and
        % end points are the third and third-last points, respectively (for
        % top and bottom). If there is an edge composed of only two points
        % (a single line segment), obviously just use the only two points
        % that are defined.
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

        % For both top and bottom extensions, compute the angle between the
        % start and the end
        top_angle = atan((top_end(1) - top_start(1)) / (top_end(2) - top_start(2)));
        bottom_angle = atan((bottom_end(1) - bottom_start(1)) / (bottom_end(2) - bottom_start(2)));
        
        % Compute the delta for each step for top and bottom, using the
        % angle between the start and end for each, and selecting the
        % current orientation based on the start and end positions with
        % respect to each other        
        if(top_start(1) > top_end(1) && top_start(2) > top_end(2))
            top_y_delta  = abs(sin(top_angle) * EXTENSION_STEP_SIZE);
            top_x_delta  = abs(cos(top_angle) * EXTENSION_STEP_SIZE);
        elseif (top_start(1) > top_end(1) && top_start(2) <= top_end(2))
            top_y_delta  = abs(sin(top_angle) * EXTENSION_STEP_SIZE);
            top_x_delta  = -1 * abs(cos(top_angle) * EXTENSION_STEP_SIZE);
        elseif (top_start(1) <= top_end(1) && top_start(2) <= top_end(2))
            top_y_delta  = -1 * abs(sin(top_angle) * EXTENSION_STEP_SIZE);
            top_x_delta  = -1 * abs(cos(top_angle) * EXTENSION_STEP_SIZE);
        elseif (top_start(1) <= top_end(1) && top_start(2) > top_end(2))
            top_y_delta  = -1 * abs(sin(top_angle) * EXTENSION_STEP_SIZE);
            top_x_delta  = abs(cos(top_angle) * EXTENSION_STEP_SIZE);
        end
        
        top_deltas(:,i) = [top_y_delta top_x_delta];
        
        % Do bottoms
        if(bottom_start(1) > bottom_end(1) && bottom_start(2) > bottom_end(2))
            bottom_y_delta  = abs(sin(bottom_angle) * EXTENSION_STEP_SIZE);
            bottom_x_delta  = abs(cos(bottom_angle) * EXTENSION_STEP_SIZE);
        elseif (bottom_start(1) > bottom_end(1) && bottom_start(2) <= bottom_end(2))
            bottom_y_delta  = abs(sin(bottom_angle) * EXTENSION_STEP_SIZE);
            bottom_x_delta  = -1 * abs(cos(bottom_angle) * EXTENSION_STEP_SIZE);
        elseif (bottom_start(1) <= bottom_end(1) && bottom_start(2) <= bottom_end(2))
            bottom_y_delta  = -1 * abs(sin(bottom_angle) * EXTENSION_STEP_SIZE);
            bottom_x_delta  = -1 * abs(cos(bottom_angle) * EXTENSION_STEP_SIZE);
        elseif (bottom_start(1) <= bottom_end(1) && bottom_start(2) > bottom_end(2))
            bottom_y_delta  = -1 * abs(sin(bottom_angle) * EXTENSION_STEP_SIZE);
            bottom_x_delta  = abs(cos(bottom_angle) * EXTENSION_STEP_SIZE);
        end
        
        bottom_deltas(:,i) = [bottom_y_delta bottom_x_delta];
        
    end
    
    % Actually do the extensions until intersection
    
    extend_further = ones(1, length(new_edgelist));
    for extendIter = 1:(MAX_EXTENSION/EXTENSION_STEP_SIZE)
        for i = 1:length(edgelist)
            cur_seg = edgelist{i};
            if(extend_further(i))
                % do the extension on both sides
                top_start       = cur_seg(1,:);
                bottom_start    = cur_seg(end,:);
                
                new_top_y = top_start(1) + top_deltas(1, i);
                new_top_x = top_start(2) + top_deltas(2, i);
                
                new_bottom_y = bottom_start(1) + bottom_deltas(1, i);
                new_bottom_x = bottom_start(2) + bottom_deltas(2, i);
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
