% find local mimima along rows
function vein_img = find_minima(isOctave, fil, vein_img)

%   figure
%   imshow(fil)
%   hold on
  all_x_prom = zeros(size(vein_img));
  all_y_prom = zeros(size(vein_img));
  
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
          
          for promLoc = 1:length(imin)
              all_x_prom(y(promLoc), imin(promLoc)) = prominences(promLoc); 
          end
          
      end
  end
  
%   for i = 1:size(fil,2)
%       if (isOctave)
%           data = cpp_smooth(fil(:,i), 4); 
%       else
%           data = smooth(fil(:,i),4);
%       end
%       data_inv = 1.01*max(data) - data;
%       [~, imin, widths, prominences] = findpeaks(data_inv);
%       
%       x_len = length(imin);
%       x = ones(1,x_len) * i;
%       
%       plot(x,imin,'g*', 'markers',1)
%       
%       if(numel(imin) > 0)
%            vein_img(sub2ind(size(vein_img), imin(:), x(:))) = 1;
% 
%            for promLoc = 1:length(imin)
%               all_y_prom(imin(promLoc), x(promLoc)) = prominences(promLoc); 
%           end
%       end
%   end

if(~isOctave)
  figure; 
  imagesc(all_x_prom,[min(min(all_x_prom(all_x_prom > 0))) max(max(all_x_prom))]); colormap(jet);
end
  %   imagesc(all_y_prom,[min(min(all_y_prom(all_y_prom > 0))) max(max(all_y_prom))]); colormap(jet);

%   disp('finished')
end
