// g++ -std=c++20 -D NAME_MAIN real_polynom_test.cpp -lgmpxx -lgmp -o main.exe && ./main.exe
# include <iostream>
using std::cout;
using std::endl;
using std::ostream;
#include <gmpxx.h>
#include <unordered_map>
using std::unordered_map;
#include <limits>
#include <array>
using std::array;
#include <complex>
//using std::complex;
#include <sstream>
using std::stringstream;
// todo exceptions https://rollbar.com/blog/cpp-custom-exceptions/#

//класс
//вывод
//хеш
//сравнение
//умножение
//доп конструкторы

template<typename T>
bool need_parentheses(const T & x) {
	return false; //<static_cast<T>(0)
}
template<>
bool need_parentheses(const int & x) {
	return x<0;
}
template<>
bool need_parentheses(const mpz_class & x) {
	return x<0;
}
// ============================== complex ===================================
#if 1
using std::complex;
#else
template<typename T>
class complex:public std::complex<T> {
public:
	complex(){}
	complex(const complex<T> &) = default;
	complex(complex<T> &&) = default;
	complex & operator=(const complex<T> &) = default;
	complex & operator=(complex<T> &&) = default;

	complex(const T & x) :std::complex<T>(x){} // ! implicit !
	complex & operator=(const T & x) {return *this = complex<T>(x);}

	complex(int x) :std::complex<T>(x){} // ! implicit !
	complex & operator=(int x) {return *this = complex<T>(x);}
};
#endif
template<typename T>
ostream & operator<<(ostream & str, const complex<T> & m){
	//return str<<"("<<m.real()<<","<<m.imag()<<")";
	if(m.real()!=0 && m.imag()!=0) {  
		if(m.imag()==1)
			return str<<m.real()<<"+"<<               "i_";
		if(m.imag()==-1)
			return str<<m.real()<<"-"<<               "i_";
		if(m.imag()<0)
			return str<<m.real()     <<m.imag()<<"*"<<"i_";
		else
			return str<<m.real()<<"+"<<m.imag()<<"*"<<"i_";
	}
	if(m.imag()!=0) {  
		if(m.imag()==1)
			return str<<           "i_";
		if(m.imag()==-1)
			return str<<          "-i_";
		//if(m.imag()<0)
			return str<<m.imag()<<"*i_";
	}
        return str<<m.real();
}
template<typename T>
bool need_parentheses(const complex<T> &m) {
	return m.real() && m.imag() || m.real()<0 || m.imag()<0;
}

complex<mpz_class> operator""_i(unsigned long long d) {
    return complex<mpz_class> {0, static_cast<mpz_class>(d)};
}
complex<mpz_class> operator""_re(unsigned long long d) {
    return complex<mpz_class> {static_cast<mpz_class>(d), 0};
}


void test_complex() {
	cout <<"__gmp_version="<< __gmp_version << endl;

	stringstream str;
	str << "=== test complex ===";
	cout<<str.str()<<endl;
	str.str("");
	cout<<str.str()<<endl;

	//тест литералов
	//тест вывода
	//тест сложения/умножения 

	auto c1 = complex<mpz_class>(1);
	cout << c1<<endl;
	//complex<mpz_class> c2 = 2;
	complex<mpz_class> c2;c2 = 2;
	cout << (c2*c1) <<" "<<(c2+c1)<<endl;

}

// ============================== Xin ===================================
class Xin {
public:
	typedef size_t deg_t;
	deg_t deg;

	Xin(): deg(0){}
	explicit Xin(int p): deg(p){}
	Xin(const Xin &) = default;
	Xin(Xin &&) = default;
	// copy/move - default
};

ostream & operator<<(ostream & str, Xin p){
	return str<<"x^"<<p.deg;
}

template<>
struct std::hash<Xin>{
	size_t operator()(Xin x) const {
		return x.deg;
	}
};

bool operator==(Xin l, Xin r){
	return l.deg == r.deg;
}

Xin operator*(Xin l, Xin r){
	if (l.deg > 0 && r.deg > std::numeric_limits<Xin::deg_t/*typeof(l.deg)*/>::max() - l.deg)
		throw "overflow in Xin";
	return Xin(l.deg + r.deg); 
}


void test_Xin() {
	// тест вывода
	// тест умножения
	// тест переполнения при умножении
}

// ============================== polynom ===================================
template <typename T>
bool is_null(const T & x) { // для определения, что коэффициент больше не нужен
	return x==static_cast<T>(0);
}

template<typename K, typename V, typename H = std::hash<V>> // Koefficient, Variable
class polynom:public unordered_map<V,K,H> { // hash...
	 //unordered_map<V,K> inner;
public:
	polynom(){}
	polynom(const polynom &) = default;
	polynom(polynom &&) = default;
	polynom<K,V,H> & operator=(const polynom<K,V,H> &) = default;
	polynom<K,V,H> & operator=(polynom<K,V,H> &&) = default;

	polynom(const K & k, const V & v) :unordered_map<V,K,H>({{v,k}}){}// inner[k] = v; // monom

	const polynom<K,V,H> & 
	operator+=(const polynom<K,V,H> & other) {
		for(auto it : other){
			if(this->contains(it.first)) {
				(*this)[it.first]+= it.second;
				if(is_null((*this)[it.first]))
					this->erase(it.first);
			}
			else
				(*this)[it.first] = it.second;
		}
		return *this;
	}
	const polynom<K,V,H> & 
	operator*=(const K & m) {
		if(is_null(m))
			this->clear();
		else
			for(auto & it : *this){
				it.second *= m;
			}
		return *this;
	}
};
template<typename K, typename V, typename H = std::hash<V>>
bool is_null(const polynom<K,V,H> & p){	
	return p.empty(); // p.size()==0
}

template<typename K, typename V, typename H = std::hash<V>>
ostream & operator<<(ostream & str, const polynom<K,V,H> & p){
	// todo сортировка
	if(is_null(p))
		return str<<'0';
	auto it = p.begin();
	if(need_parentheses(it->second))
		str<<"("<<(it->second)<<")"<<'*'<<(it->first);// k*v
	else
		str<<(it->second)<<'*'<<(it->first);// k*v
	for(it++; it!=p.end(); it++){
		if(need_parentheses(it->second))
			str<<" + "<<(it->second)<<'*'<<(it->first);// k*v
		else
			str<<" + "<<(it->second)<<'*'<<(it->first);// k*v
	}
	return str;
}
template<typename K, typename V, typename H = std::hash<V>>
bool need_parentheses(const polynom<K,V,H> & p) {
	return p.size()>1;
}

template<typename K, typename V, typename H = std::hash<V>>
polynom<K,V,H>
operator*(const polynom<K,V,H> & l, const polynom<K,V,H> & r) {
	// multithread optimizations here
	// лучше сделать отдельную специализацию метода
	polynom<K,V,H> result;
	for(auto it1 : l)
		for(auto it2 : r){
			auto tmp_v = it1.first * it2.first;
			auto tmp_k = it1.second * it2.second;
			result += std::move(tmp_k)*std::move(tmp_v);//polynom<K,V,H>(tmp_k,tmp_v); // todo : optimize : polynom+=pair
		}
	return std::move(result);
}
template<typename K, typename V, typename H = std::hash<V>>
polynom<K,V,H>
operator*(polynom<K,V,H> && l, V && r) {
	polynom<K,V,H> tmp;
	for(auto x : l){
		tmp[x.first*r] = x.second; // assume surjection (different to different) in ring V
	}
	return std::move(tmp);
}
template<typename K, typename V, typename H = std::hash<V>>
polynom<K,V,H>
operator*(polynom<K,V,H> && l, K && r) {
	return l*=r;
}

template<typename K, typename V, typename H = std::hash<V>>
polynom<K,V,H> operator+(const polynom<K,V,H> & l, const polynom<K,V,H> & r) {
	polynom<K,V,H> tmp = l;
	return std::move(tmp+=r);
}// deafult

/* too common
template<typename K, typename V>
polynom<K,V> operator*(K && k, V && v){
	return polynom<K,V>(k,v);
}
*/
polynom<complex<mpz_class>,Xin> operator*(complex<mpz_class> && k, Xin && v){
	return polynom<complex<mpz_class>,Xin>(k,v);
}
polynom<mpz_class,Xin> operator*(mpz_class && k, Xin && v){
	return polynom<mpz_class,Xin>(k,v);
}
// ============================== FinMon ===================================

template<int N> 
class FinMon : public array<size_t,N> { // finit monom
public:
	typedef size_t deg_t;

	FinMon(const FinMon &) = default;
	FinMon(FinMon &&) = default;
	FinMon & operator=(const FinMon &) = default;
	FinMon & operator=(FinMon &&) = default;

	FinMon() { 
		for(int i=0; i<N; i++) (*this)[i]=0;
	}
	FinMon(int n, int d){
 		for(int i=0; i<N; i++) (*this)[i]=0;
 		(*this)[n]=d;
	}

	FinMon<N> 
	operator*=(const FinMon<N> & other){
		for(int i=0; i<N; i++)
			(*this)[i]+=other[i];
		return * this;
	}
};
template<int N>
FinMon<N> operator*(const FinMon<N> & l, const FinMon<N> & r){
	FinMon<N> tmp = l;
	return std::move(tmp*=r);
}
template<int N>
struct std::hash<FinMon<N>>{
	size_t operator()(const FinMon<N> & x) const {
		typename FinMon<N>::deg_t q=x[0];
		for(int i=1; i<N; i++)
			q = (q<<1)^x[i];
		return q;
	}
};

// ============================== Locals ===================================
#ifdef NAME_MAIN
// x,y,z,a,b
#define monsize 5
polynom<complex<mpz_class>,FinMon<monsize>> operator*(complex<mpz_class> && k, FinMon<monsize> && v){
	return polynom<complex<mpz_class>,FinMon<monsize>>(k,v);
}

polynom<mpz_class,FinMon<monsize>> operator*(mpz_class && k, FinMon<monsize> && v){
	return polynom<mpz_class,FinMon<monsize>>(k,v);
}

FinMon<monsize> x_in(int p){ return FinMon<monsize>(0,p); }
FinMon<monsize> y_in(int p){ return FinMon<monsize>(1,p); }
FinMon<monsize> z_in(int p){ return FinMon<monsize>(2,p); }
FinMon<monsize> a_in(int p){ return FinMon<monsize>(3,p); }
FinMon<monsize> b_in(int p){ return FinMon<monsize>(4,p); }
int x_(const FinMon<monsize> & m){ return m[0]; }
int y_(const FinMon<monsize> & m){ return m[1]; }
int z_(const FinMon<monsize> & m){ return m[2]; }
int a_(const FinMon<monsize> & m){ return m[3]; }
int b_(const FinMon<monsize> & m){ return m[4]; }

ostream & operator<<(ostream & str, const FinMon<monsize> m){
	const char * names[monsize] = {"x","y","z","a","b",};
	bool start = true;
	for(int i=0; i<monsize; i++){
		if(m[i]){
			if(!start)  str<<"*";
			            str<<names[i];
			if(m[i]!=1) str<<"^"<<m[i];
			start = false;
		}
	}
	if(start) str<<1;
	return str;
}


//template<>
//complex<mpz_class>::complex(const mpz_class & x){cout<<"c-tor"<<endl;}

int main() {
	cout<<endl;
	{
		FinMon<5> x;
		cout << x <<endl;
		auto y = y_in(5);
		cout << y <<endl;
		auto yz = y_in(5)*z_in(2);
		cout << yz <<endl;
		auto p1 = 5_i*x_in(1);
		cout << p1<<endl;;
		auto p2 = 5_re*x_in(1)*z_in(2);
		cout << p2<<endl;
		auto p3 = p1+p2;
		cout << p3<<endl;
		cout << p3*p3<<endl;
		auto p4 = 1_re*a_in(1)+1_re*b_in(1);
		auto p5 = 1_re*a_in(0);
		for(int i=1; i<10; i++) {
			p5 = p5*p4;
			cout<<i<<" : "<<p5<<endl;
		}
	}
	cout<<endl;
	{
		auto x = Xin(5), y=Xin(6);
		cout << x*y<<endl;
		auto aa = Xin(2);
		auto ab = mpz_class(3);
		unordered_map<Xin,mpz_class> q({{aa,ab}});
		//unordered_map<int,int> q = {{3,4}};
		polynom<mpz_class,Xin> za = {3,Xin(5)};
		polynom<mpz_class,Xin> zb = {4,Xin(2)};
		auto z= za+zb;
		z = 3*Xin(5) + 4*Xin(6);
		cout << z << endl;
		polynom<mpz_class,Xin> zz = 
		z*z;
		cout << z*z << endl;
		polynom<int,int> i;
		i*i;
	}
	cout<<endl;
	{
		mpz_class a, b, c;	
		a = 1234;
		b = "-5678";
		c = a+b;
		cout << "sum is " << c << "\n";
		cout << "absolute value is " << abs(c) << "\n";
	}
}
#endif