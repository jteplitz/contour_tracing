function length = segment_length(segments)
    length = 0;
    for i = 1:size(segments,1)-1
        length = length + pdist([segments(i,:); segments(i+1,:)]);
    end
end
