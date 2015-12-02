function do_bvg(inFile, outFile)


    
    isOctave = exist('OCTAVE_VERSION', 'builtin') ~= 0;
    
     image = imread(inFile);
    
     if(ndims(image) > 2)    
        img_gray = rgb2gray(image);
    else
        img_gray = image;
    end

    fil_img = uint8(imfilter(double(img_gray), ones(30) / 900, 'replicate'));

    small = imresize(fil_img, .25);
    img_size = size(small);
    fil = im2double(small);
    vein_img = zeros(size(fil, 1), size(fil, 2));


    vein_img = find_minima(isOctave, fil, vein_img);
    minima = vein_img; 

    % remove the junk on the image edges
    vein_img(:,end-3:end) = 0;  
    vein_img(:,1:3) = 0;
    vein_img(end-3:end,:) = 0;  
    vein_img(1:3,:) = 0;
    
%     vein_img_filled = filledgegaps(vein_img, 3);
%     vein_img_cleaned = bwareaopen(vein_img_filled, 10);
%     vein_img_connected = filledgegaps(vein_img_cleaned, 7);
%     [edgelist, ~] = edgelink(vein_img_connected, 1);

    vein_img = bwareaopen(vein_img, 5); % prev 5
    vein_img = filledgegaps(vein_img, 4);
    vein_img = bwareaopen(vein_img, 10);
    [edgelist, ~] = edgelink(vein_img, 1);
    
    %subplot(2,2,4)
    %drawedgelist(edgelist, size(fil), 1, 'rand');
    
    extend_edgelist = extend_veins(edgelist, img_size);
    
    %subplot(2,2,2)
    % drawedgelist(extend_edgelist, size(fil), 1, 'rand');
    
    export_edgelist(extend_edgelist, outFile, img_size);

 %   imshow(minima)
 %   pause(100)
end
