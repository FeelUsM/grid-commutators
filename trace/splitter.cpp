#include <iostream>
#include <stdlib.h>
#include <string.h>
#include <fstream>
#include <string>

using namespace std;

char read_until(ofstream & out, ifstream & in, const char * stop_symbols) {
	char c=0;
	while(!in.eof()) {
		in.get(c);
		out<<c;
		if(strchr(stop_symbols,c))
			break;
		c=0;
	}
	return c;
}

char read_brackets(ofstream & out, ifstream & in) {
	char c;
	while(true) {
		c = read_until(out,in,"()");
		if(c==')' || c==0)
			break;
		else
			read_brackets(out,in);
	}
	return c;
}

int main(int argc, char * argv[]) {
	if(argc!=4) {
		cerr << "syntax: splitter file max_len out_base"<<endl;
		exit(1);
	}

	string outbase = argv[3];

	char * pc;
	errno=0;
	long max_len = strtol(argv[2],&pc,10);
	if(pc-argv[2]!=strlen(argv[2]) || errno) {
		cerr<<"can't read max_len"<<endl;
		cerr<<pc-argv[2]<<" "<<strlen(argv[2])<<" "<<pc<<endl;
		exit(1);
	}
	
	ifstream input;
	if(strcmp(argv[1],"--")==0) {
		cin.rdbuf(input.rdbuf());
		//input.rdbuf(cin.rdbuf());
		//input = cin;
	}
	else {
		input.open(argv[1]);
	}
	
	//if(input.eof()) - не рассматриваем
	//input>>curc;
	
	int outcount = 0;
	while(!input.eof()) {
		outcount++;
		ofstream output(outbase+to_string(outcount));
		
		cout<<"L L = L"<<endl
		<<"#include - "<<(outbase+to_string(outcount))<<endl
		<<";"<<endl
		<<".sort"<<endl;
		
		for(int incount=0; incount<max_len && !input.eof(); incount++) {
			char c;
			c = read_until(output,input,"S(");
			if(c==0) break;
			if(c=='S')
				c = read_until(output,input,"(");
			if(c==0) break;
			c = read_brackets(output,input);
			if(c==0) break;
			
			c = read_until(output,input,"(");
			if(c==0) break;
			c = read_brackets(output,input);
			if(c==0) break;
		}
	}
	
}