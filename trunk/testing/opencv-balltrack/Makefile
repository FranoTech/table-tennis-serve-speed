CC=g++

all: 
	 $(CC) `pkg-config opencv --cflags` opencv-balltrack.cpp -o balltrack `pkg-config --libs opencv`

clean: 
	rm -rf *.o balltrack

