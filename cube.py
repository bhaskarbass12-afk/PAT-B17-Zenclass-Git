L,B,H = map(int,input().split())
area = L*B
area2 = B*H
area3 = L*H
overall=2*(area+area2+area3)
volume = L*B*H
print(volume, overall)