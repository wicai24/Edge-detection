
arr = imageio.imread('images.jpg')
angels=np.zeros((256, 256))
def greyscale_conversion(arr):
	for x in range(256):
		for y in range(256):
			arr[x,y]=0.299*arr[x,y,0] + 0.587*arr[x,y,1] + 0.114*arr[x,y,2]

def gaussian_kernel(size,sigma=1):
	sum=0
	Filter= [[0 for x in range(size*2)] for y in range(size*2)]
	for x in range(-size,size):
		for y in range(-size,size):
			Filter[x+size][y+size]=(1/(2*math.pi*sigma*sigma))*math.exp(-(x*x+y*y)/2*sigma*sigma)
			sum+=Filter[x+size][y+size]
	for i in range(size*2):
		for j in range(size*2):
			Filter[i][j]/=sum
	return Filter

def gaussian_filter(arr,kernel,w,h):
	newarr=np.zeros((256, 256))
	for x in range(4,w-4):
		for y in range(4,h-4):
			value = 0
			for x2 in range(4):
				for y2 in range(4):
					value+=kernel[x2][y2]*arr[x+x2-4,y+y2-4,0]
			newarr[x+x2-4,y+y2-4]=value
	return newarr

def sobel_filters(arr,w,h):
	newarr=np.zeros((256, 256))
	xfilter=[[-1,0,1],[-1,0,1],[-1,0,1]]
	yfilter=[[1,1,1],[0,0,0],[-1,-1,-1]]
	for x in range(5,w-5):
		for y in range(5,h-5):
			sumx=0
			sumy=0
			gradient=0
			for x2 in range(3):
				for y2 in range(3):
					sumx+=xfilter[x2][y2]*arr[x+x2-4,y+y2-4]
					sumy+=yfilter[x2][y2]*arr[x+x2-4,y+y2-4]
			dist=math.sqrt((sumx*sumx)+(sumy*sumy))
			if dist> 255:
				dist =255
			newarr[x,y]=dist
			angels[x][y]=math.atan2(sumy,sumx)* 180/math.pi
	return newarr
	
def non_max_suppression(arr,angels,w,h):
	p1=0
	p2=0
	p3=0
	p4=0
	newarr=np.zeros((256, 256))
	for x in range(5,w-5):
		for y in range(5,h-5):
			if 0<=angels[x][y] and angels[x][y]<=90:
				p1=arr[x][y-1]
				p2=arr[x][y+1]
				p3=arr[x-1][y+1]
				p4=arr[x+1][y-1]
			elif 0>angels[x][y] and angels[x][y]>=(-90):
				p1=arr[x][y-1]
				p2=arr[x][y+1]
				p3=arr[x+1][y+1]
				p4=arr[x-1][y-1]
			if arr[x][y]>p1 and arr[x][y]>p2 and arr[x][y]>p3 and arr[x][y]>p4:	# if local maximum
				print("TRIGGERED", x, y)
				newarr[x][y]=arr[x][y]
			else: newarr[x][y]=0 
	return newarr

def double_threshold(arr,w,h,low,high):
	newarr=np.zeros((256, 256))
	for x in range(w):
		for y in range(h):
			if arr[x][y]>=high:
				newarr[x][y]=255
			elif arr[x][y]<=low:
				newarr[x][y]=0
			elif arr[x-1][y+1]>=high or arr[x][y+1]>=high or arr[x+1][y+1]>=high or arr[x-1][y]>=high or arr[x+1][y]>=high or arr[x-1][y-1]>=high or arr[x][y-1]>=high or arr[x+1][y-1]>=high:
				newarr[x][y]=255
			else:
				newarr[x,y]=0
	return newarr

greyscale_conversion(arr)
imageio.imwrite('test.png', sobel_filters(gaussian_filter(arr,gaussian_kernel(2),256,256),256,256))
imageio.imwrite('gradient.png', double_threshold(non_max_suppression(sobel_filters(gaussian_filter(arr,gaussian_kernel(2),256,256),256,256),angels,256,256),256,256,60,80))