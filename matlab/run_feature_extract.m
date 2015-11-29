isOctave = exist('OCTAVE_VERSION', 'builtin') ~= 0;
if (isOctave)
	pkg load image
end
profile on
%% jason L
path = '~/contour_tracing/images/';
fileList = {'jason.crop.1447554716.jpg', 'jason.crop.1447554743.jpg', 'jason.crop.1447554776.jpg'};

edgelist = feature_extract(strcat(path, fileList{1}))
%%
T = profile("info");
profshow(T)
%profexplore(T)

new_edgelist = extend_veins(edgelist);
figure
drawedgelist(new_edgelist, [0,0], 1, 'rand')
%%
%for fileNum = 1:length(fileList)
%    edgelist = feature_extract(strcat(path, fileList{fileNum}))
%end 
%%
%edgelist = feature_extract('/Users/rishi/Google Drive/Biometric Vascular Gateway/Vein Pics/class pics/bora.1448076037.crop.jpg');
