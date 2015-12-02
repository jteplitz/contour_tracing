% find local mimima along rows
function vein_img = find_minima(isOctave, fil, vein_img)

%   figure
%   imshow(fil)
%   hold on
  for i = 1:size(fil,1)
      if (isOctave)
            data = cpp_smooth(fil(i,:),2);
      else
            data = smooth(fil(i,:),2);
      end
      
      data_inv = 1.01*max(data) - data;
      [~, imin, widths, prominences] = findpeaks(data_inv);
      
      y_len = length(imin);
      y = ones(1,y_len) * i;
      
%       plot(imin,y,'g*', 'markers',1)
      
      if(numel(imin) > 0)       
          vein_img(sub2ind(size(vein_img), y(:), imin(:))) = 1;
      end
  end
  
  for i = 1:size(fil,2)
      if (isOctave)
          data = cpp_smooth(fil(:,i), 4); 
      else
          data = smooth(fil(:,i),4);
      end
      data_inv = 1.01*max(data) - data;
      [~, imin] = findpeaks(data_inv);
      
      x_len = length(imin);
      x = ones(1,x_len) * i;
      
%       plot(x,imin,'g*', 'markers',1)
      
      if(numel(imin) > 0)
           vein_img(sub2ind(size(vein_img), imin(:), x(:))) = 1;
      end
  end
  
end
