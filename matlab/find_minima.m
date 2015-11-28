% find local mimima along rows
function vein_x_img = find_minima(isOctave, fil, vein_x_img)
  for i = 1:size(fil,1)
      if (isOctave)
          [ymax,imax,ymin,imin] = extrema(cpp_smooth(fil(i,:), 9)); % previously 10
      else
          [ymax,imax,ymin,imin] = extrema(smooth(fil(i,:), 9)); % previously 10
      end
      
      y_len = length(imin);
      y = ones(1,y_len) * i;
      %plot(imin,y,'g*', 'markers',1)
      
      if (isOctave)
          vein_x_img(sub2ind(size(vein_x_img), y', imin')) = 1;
      else
          vein_x_img(sub2ind(size(vein_x_img), y', imin)) = 1;
      end
  end
end
