fid = fopen("NE.txt", 'r');
[A,nelem] = fscanf(fid,'%d');
nelem = nelem/3;
fid = fopen("NE.txt", 'r');
E2N = fscanf(fid,'%d',[3 nelem]);
E2N = E2N';

% fid = fopen("square_E2N.txt", 'r');
% [A,nelem] = fscanf(fid,'%d');
% nelem = nelem/3;
% fid = fopen("square_E2N.txt", 'r');
% E2N = fscanf(fid,'%d',[3 nelem]);
% E2N = E2N';

nnode = max(max(E2N));
H = sparse(nnode,nnode); 
HH = sparse(nnode,nnode); 
IE = zeros(ceil(nelem*3/2), 4); 
I2E = zeros(ceil(nelem*3/2), 4); 
niedge = 0;                     
face = zeros(nelem,3);
nf = 0;
for elem = 1:nelem
  nv = E2N(elem,1:3);
  for edge = 1:3
    n1 = nv(mod(edge  ,3)+1);
    n2 = nv(mod(edge+1,3)+1);
    oppositenode = edge;
    if (H(n1,n2) == 0)
      H(n1,n2) = elem;  H(n2,n1) = elem;
      HH(n1,n2) = oppositenode;  HH(n2,n1) = oppositenode;
    else
      oldelem = H(n1,n2);
      oldoppositenode = HH(n1,n2);
      if (oldelem < 0), error 'Mesh input error'; end
      niedge = niedge+1;
      IE(niedge,:) = [n2,n1, oldelem, elem];
      I2E(niedge,:) = [oldelem, oldoppositenode, elem, oppositenode];
      H(n1,n2) = -1;  H(n2,n1) = -1;
      HH(n1,n2) = -1;  HH(n2,n1) = -1;
    end
  end
end

IE = IE(1:niedge,:);  
I2E = I2E(1:niedge,:); % clip I2E


[I,J] = find(triu(H)>0);  
BE = [I, J, zeros(size(I))];

g1 = 1:40;
g2 = 41:80;
g3 = 81:120;
g4 = 125:128;
g5 = 129:132;
g6 = 133:136;
g7 = 137:140;


for i = 1:size(BE)
    if any(ismember(BE(i,1:2),g1) == 1)
        BE(i,3) = 1;
    elseif any(ismember(BE(i,1:2),g2) == 1)
        BE(i,3) = 2;
    elseif any(ismember(BE(i,1:2),g3) == 1)
        BE(i,3) = 3; 
    elseif any(ismember(BE(i,1:2),g4) == 1)
        BE(i,3) = 4;
    elseif any(ismember(BE(i,1:2),g5) == 1)
        BE(i,3) = 5; 
    elseif any(ismember(BE(i,1:2),g6) == 1)
        BE(i,3) = 6; 
    elseif any(ismember(BE(i,1:2),g7) == 1)
        BE(i,3) = 7;     
    end
end

for b = 1:size(I,1)
    BE(b, 1) = H(I(b),J(b));
    BE(b, 2) = HH(I(b),J(b));
end
B2E = BE;
% save("B2E.txt","B2E",'-ascii')
% save("I2E.txt","I2E",'-ascii')