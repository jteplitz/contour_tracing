%% Turn profiler on for Octave
isOctave = exist('OCTAVE_VERSION', 'builtin') ~= 0;
if (isOctave)
	pkg load image
    profile on
end

%% Set path of images
path = '../images/';
output_path = '../output/';

%% Jason's left hand
fileList = {'jason.crop.1447554716.jpg', 'jason.crop.1447554743.jpg', 'jason.crop.1447554776.jpg'};

%% Bora's ? hand
fileList = {'bora.1448076037.jpg', 'bora.1448076067.jpg', 'bora.1448076098.jpg'};

%% Run all images in the fileList
for fileNum = 1:length(fileList)
    [edgelist, img_size] = feature_extract(strcat(path, fileList{fileNum}));
    new_edgelist = extend_veins(edgelist, img_size);
    figure
    drawedgelist(new_edgelist, [0,0], 1, 'rand')
    filtered_edgelist = length_filter(edgelist, 60);
    figure
    drawedgelist(filtered_edgelist, [0,0], 1, 'rand')
    export_edgelist(filtered_edgelist, [output_path fileList{fileNum} '_not_connected.csv'], img_size);
    export_edgelist(new_edgelist, [output_path fileList{fileNum} '_connected.csv'], img_size);
end

%% Profiler for Octave
if (isOctave)
    T = profile('info');
    profshow(T)
    %profexplore(T)
end