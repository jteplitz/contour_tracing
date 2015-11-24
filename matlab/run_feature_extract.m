%% jason L
path = '/Users/rishi/Google Drive/Biometric Vascular Gateway/Vein Pics/class pics/Jason/L/';
fileList = {'jason.crop.1447554690.jpg', 'jason.crop.1447554716.jpg', 'jason.crop.1447554743.jpg', 'jason.crop.1447554776.jpg'};

edgelist = feature_extract(strcat(path, fileList{1}))
%%

new_edgelist = extend_veins(edgelist);

%%
for fileNum = 1:length(fileList)
    edgelist = feature_extract(strcat(path, fileList{fileNum}))
end 
%%
edgelist = feature_extract('/Users/rishi/Google Drive/Biometric Vascular Gateway/Vein Pics/class pics/bora.1448076037.crop.jpg');
