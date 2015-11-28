% Voting to remove isolated points
function copy = vote(vein_x_img)
  copy = vein_x_img(:,:);
  for i = 2:size(vein_x_img, 1)-1
      for j = 2:size(vein_x_img,2)-1
          sel = (vein_x_img(i-1:i+1,j-1:j+1));
          selSum = sum(sel(:));
          if (selSum > 1)
              copy(i,j) = 1;
          else
              copy(i,j) = 0;
          end
      end
  end
end
