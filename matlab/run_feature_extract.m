%% jason L
path = '/Users/rishi/Google Drive/Biometric Vascular Gateway/Vein Pics/class pics/Jason/L/'
fileList = {'jason.crop.1447554690.jpg', 'jason.crop.1447554716.jpg', 'jason.crop.1447554743.jpg', 'jason.crop.1447554776.jpg'};
%%
for fileNum = 1:length(fileList)
    feature_extract(strcat(path, fileList{fileNum}));
end 