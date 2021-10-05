#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

char read_until(FILE * out, FILE * in, const char * stop_symbols) {
	//printf("read_until %s\n",stop_symbols);
	char c=0;
	while(!feof(in)) {
		c = fgetc(in);
		//printf("%c %d\n",c,c);
		fputc(c,out);
		if(strchr(stop_symbols,c))
			break;
		c=0;
	}
	return c;
}

char read_brackets(FILE * out, FILE * in) {
	//printf("read_brackets\n");
	char c;
	while(1) {
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
		fprintf(stderr,"syntax: splitter file max_len out_base\n");
		exit(1);
	}

	char * pc;
	errno=0;
	long max_len = strtol(argv[2],&pc,10);
	if(pc-argv[2]!=strlen(argv[2]) || errno) {
		fprintf(stderr,"can't read max_len\n");
		fprintf(stderr,"%d %d %s\n",pc-argv[2],strlen(argv[2]),pc);
		exit(1);
	}
	
	FILE * input;
	if(strcmp(argv[1],"--")==0) {
		//cin.rdbuf(input.rdbuf());
		//input.rdbuf(cin.rdbuf());
		input = stdin;
	}
	else {
		input = fopen(argv[1],"r");
	}
	//printf("%d\n",input);
	
	//if(input.eof()) - не рассматриваем
	//input>>curc;
	
	int outcount = 0;
	while(!feof(input) && outcount<10) {
		outcount++;

		char outname[10000];
		char outcount_s[10000];
		sprintf(outname,"%s%d",argv[3],outcount);
		FILE * output = fopen(outname,"w");
		
		printf("L L = L\n");
		printf("#include - %s\n",outname);
		printf(";\n");
		printf(".sort\n");
		
		for(int incount=0; incount<max_len && !feof(input); incount++) {
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