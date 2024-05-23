// g++ -std=c++20 commute_2d.cpp -lgmpxx -lgmp -o main.exe && ./main.exe
#include "real_polynom_test.cpp"
using std::pair;
using std::make_pair;
#include <tuple>
using std::tuple;
using std::get;
#include <initializer_list>
#include <algorithm>
using std::max;
#include <cassert>
#include <vector>
using std::vector;
#include <string.h>

template<typename K, typename V, typename H = std::hash<V>>
polynom<K,V,H>
commute(const polynom<K,V,H> & l, const polynom<K,V,H> & r) {
	polynom<K,V,H> result;
	for(auto it1 : l)
		for(auto it2 : r){
			auto 
			tmp_v = it1.first  * it2.first;
			tmp_v*=  (it1.second * it2.second);
			result += tmp_v;

			tmp_v = it2.first  * it1.first;
			tmp_v*= -(it2.second * it1.second);
			result += tmp_v;
		}
	return std::move(result);
}

// ============================== cigma ===================================
#if 0
enum cigma : char{
	c1='0',cx,cy,cz
};
#else
class cigma {
public:
	typedef char inner_t;
	typedef complex<mpz_class> koef_t;
	inner_t inner = '0'; // всё ради конструктора по умолчанию
	operator inner_t()const { return this->inner; }
	cigma(){}
	cigma(inner_t c):inner(c){}
	bool operator==(const cigma & other)const = default;
};
const cigma c1 = cigma();
const cigma cx = cigma() + 1;
const cigma cy = cigma() + 2;
const cigma cz = cigma() + 3;
template<>
struct std::hash<cigma>{
	size_t operator()(cigma x) const {
		return x.inner;
	}
};

#endif
ostream & operator<<(ostream & str, cigma c) {
	if(c==c1) return str<<"c1";
	if(c==cx) return str<<"cx";
	if(c==cy) return str<<"cy";
	if(c==cz) return str<<"cz";
	return str<<"error";
}
pair<complex<mpz_class>,cigma> operator*(cigma l, cigma r) {
	if(l==cx && r==cx) return make_pair( 1_re ,c1);
	if(l==cx && r==cy) return make_pair( 1_i  ,cz);
	if(l==cx && r==cz) return make_pair(-1_i  ,cy);
	if(l==cy && r==cx) return make_pair(-1_i  ,cz);
	if(l==cy && r==cy) return make_pair( 1_re ,c1);
	if(l==cy && r==cz) return make_pair( 1_i  ,cx);
	if(l==cz && r==cx) return make_pair( 1_i  ,cy);
	if(l==cz && r==cy) return make_pair(-1_i  ,cx);
	if(l==cz && r==cz) return make_pair( 1_re ,c1);
	if(l==c1)          return make_pair( 1_re ,r );
	/*if(r==c1)*/      return make_pair( 1_re ,l );
}
ostream & operator<<(ostream & str, pair<complex<mpz_class>,cigma> q) {
	return str<<q.first<<"*"<<q.second;
}

template<typename K>
polynom<K,cigma>
commute(const polynom<K,cigma> & l, const polynom<K,cigma> & r) {
	polynom<K,cigma> result;
	for(auto it1 : l)
		for(auto it2 : r){
			auto 
			tmp_v = it1.first  * it2.first;
			auto 
			tmp_k = it1.second * it2.second;
			result += polynom<K,cigma>(   tmp_k*tmp_v.first , tmp_v.second);

			tmp_v = it2.first  * it1.first;
			tmp_k = it2.second * it1.second;
			result += polynom<K,cigma>( - tmp_k*tmp_v.first , tmp_v.second);
		}
	return std::move(result);
}

template<typename TA, typename TB>
polynom<polynom<TA,TB>,cigma> operator*(polynom<TA,TB> && p, pair<TA,cigma> && v){
	return polynom<polynom<TA,TB>,cigma>(std::move(p)*std::move(v.first),std::move(v.second));
}
// ============================== string operator 2d 0.5s ===================================

typedef cigma spin_t;
//template<typename spin_t>
class StringOperator2d {
	spin_t::inner_t * buf; // char
public:
	typedef spin_t spin_t;
	typedef spin_t::inner_t inner_t; // char
	typedef spin_t::koef_t koef_t;
	typedef unsigned local_size_t;
	const local_size_t w1;
	const local_size_t w2;
	StringOperator2d(const StringOperator2d & other) // != default;
		:w1(other.w1),w2(other.w2) 
	{
		buf = new inner_t[w1*w2];
		memcpy(this->buf,other.buf, w1*w2*sizeof(inner_t) );
	}
	StringOperator2d & operator=(const StringOperator2d & other) { // != default;
		delete this->buf;
		const_cast<local_size_t &>(w1) = other.w1;
		const_cast<local_size_t &>(w2) = other.w2;
		buf = new inner_t[w1*w2];
		memcpy(this->buf,other.buf, w1*w2*sizeof(inner_t) );
		return *this;
	}
	StringOperator2d(StringOperator2d && other) // != default
		:w1(other.w1),w2(other.w2) 
	{
		this->buf = other.buf;
		other.buf = nullptr;
	}
	StringOperator2d & operator=(StringOperator2d && other) { // != default
		delete this->buf;
		const_cast<local_size_t &>(w1) = other.w1;
		const_cast<local_size_t &>(w2) = other.w2;
		this->buf = other.buf;
		other.buf = nullptr;
		return *this;
	}
	~StringOperator2d() {delete buf;}
	StringOperator2d():w1(0),w2(0){
		buf = new inner_t[w1*w2];
	}
	StringOperator2d(local_size_t h1, local_size_t h2)
		:w1(h1),w2(h2) 
	{
		if (h1 != 0 && h2 > std::numeric_limits<local_size_t>::max() / h1)
			throw "overflow in StringOperator2d";
		buf = new inner_t[w1*w2];
		for(int i=0; i<w1*w2; i++) // todo for(int i : range(5))
			buf[i] = spin_t();
	}
	StringOperator2d(std::initializer_list<tuple<spin_t,local_size_t,local_size_t>> l)
		:w1(0),w2(0) 
	{
		local_size_t h1=0;
		for(auto t : l)
			if(get<1>(t)>h1)
				h1 = get<1>(t); // todo max()
		local_size_t h2=0;
		for(auto t : l)
			if(get<2>(t)>h1)
				h2 = get<2>(t); // todo max()
		const_cast<local_size_t &>(w1) = h1;
		const_cast<local_size_t &>(w2) = h2;
		buf = new inner_t[w1*w2];
		for(int i=0; i<w1*w2; i++) // todo for(int i : range(5))
			buf[i] = spin_t();
		for(auto t : l) {
			(*this)(get<1>(t),get<2>(t)) = get<0>(t);
		}
	}
	const spin_t & operator()(local_size_t x1, local_size_t x2)const { // indexing starts with 1
		//return buf[(x1-1)*w2+x2-1];
		return reinterpret_cast<spin_t &>(buf[(x1-1)*w2+x2-1]);
	}
	spin_t & operator()(local_size_t x1, local_size_t x2) { // indexing starts with 1
		return reinterpret_cast<spin_t &>(buf[(x1-1)*w2+x2-1]);
	}
	friend struct std::hash<StringOperator2d>;
};
ostream & operator<<(ostream & str, const StringOperator2d & op){
	bool start = true;
	for(StringOperator2d::local_size_t i1 = 1; i1<=op.w1; i1++)
		for(StringOperator2d::local_size_t i2 = 1; i2<=op.w2; i2++) {
			if(op(i1,i2)!=StringOperator2d::spin_t()){
				if(!start) 
					str<<"*";
				str<<op(i1,i2)<<"("<<i1<<","<<i2<<")";
				start = false;
			}
		}
	if(start)
		str<<"1";
	return str;
}
//https://github.com/gcc-mirror/gcc/blob/master/libstdc%2B%2B-v3/libsupc%2B%2B/hash_bytes.cc#L136
inline std::size_t
unaligned_load(const char* p) {
	std::size_t result;
	memcpy(&result, p, sizeof(result));
	return result;
}
inline std::size_t
shift_mix(std::size_t v) { 
	return v ^ (v >> 47);
}
inline std::size_t
load_bytes(const char* p, int n) {
	std::size_t result = 0;
	--n;
	do
		result = (result << 8) + static_cast<unsigned char>(p[n]);
	while (--n >= 0);
	return result;
}
// Implementation of Murmur hash for 64-bit size_t.
size_t
_Hash_bytes(const char* buf, size_t len, size_t seed) {
	static const size_t mul = (((size_t) 0xc6a4a793UL) << 32UL)
		+ (size_t) 0x5bd1e995UL;
	//const char* const buf = static_cast<const char*>(ptr);

	// Remove the bytes not divisible by the sizeof(size_t).  This
	// allows the main loop to process the data as 64-bit integers.
	const size_t len_aligned = len & ~(size_t)0x7;
	const char* const end = buf + len_aligned;
	size_t hash = seed ^ (len * mul);
	for (const char* p = buf; p != end; p += 8)
	{
		const size_t data = shift_mix(unaligned_load(p) * mul) * mul;
		hash ^= data;
		hash *= mul;
	}
	if ((len & 0x7) != 0)
	{
		const size_t data = load_bytes(end, len & 0x7);
		hash ^= data;
		hash *= mul;
	}
	hash = shift_mix(hash) * mul;
	hash = shift_mix(hash);
	return hash;
}
template<>
struct std::hash<StringOperator2d>{
	size_t operator()(const StringOperator2d & x) const {
		size_t h = (x.w1<<1) ^ x.w2;
		return _Hash_bytes(x.buf, x.w1*x.w2, h);
	}
};
bool operator==(const StringOperator2d & l, const StringOperator2d & r) {
	if(l.w1!=r.w1 || l.w2!=r.w2) return false;
	for(StringOperator2d::local_size_t i1 = 1; i1<=l.w1; i1++)
	for(StringOperator2d::local_size_t i2 = 1; i2<=l.w2; i2++)
		if(l(i1,i2)!=r(i1,i2))
			return false;
	return true;
}
polynom<StringOperator2d::koef_t,StringOperator2d>
operator*(StringOperator2d::koef_t && k, StringOperator2d && v){
	return polynom<StringOperator2d::koef_t,StringOperator2d>(k,v);
}

pair<StringOperator2d::koef_t,StringOperator2d>
pairwaise_mul(const StringOperator2d & lhs, StringOperator2d::local_size_t ls1, StringOperator2d::local_size_t ls2, 
	const StringOperator2d & rhs, StringOperator2d::local_size_t rs1, StringOperator2d::local_size_t rs2){
	StringOperator2d::koef_t koef {1};//explicit init
	assert(ls1==0 || rs1==0);
	assert(ls2==0 || rs2==0);
	StringOperator2d result{max(lhs.w1+ls1,rhs.w1+rs1) , max(lhs.w2+ls2,rhs.w2+rs2)};
	for(StringOperator2d::local_size_t i1=1; i1<=result.w1; i1++)
	for(StringOperator2d::local_size_t i2=1; i2<=result.w2; i2++) {
		auto li1 = i1-ls1;
		auto li2 = i2-ls2;
		auto ri1 = i1-rs1;
		auto ri2 = i2-rs2;
		#define lcheck li1>=1 && li1<=lhs.w1 && li2>=1 && li2<=lhs.w2
		#define rcheck ri1>=1 && ri1<=rhs.w1 && ri2>=1 && ri2<=rhs.w2
		if(lcheck && rcheck) {
			auto tmp = lhs(li1,li2)*rhs(ri1,ri2);
			result(i1,i2) = tmp.second;
			koef*=tmp.first;
		}
		else if(lcheck)
			result(i1,i2)=lhs(li1,li2);
		else if(rcheck)
			result(i1,i2)=rhs(ri1,ri2);
		#undef lcheck
		#undef rcheck
	}
	// trim
	StringOperator2d::local_size_t d1=1;
	if(ls1==0 && rs1==0) {
		//left trim
		bool flag = true;
		while(flag && d1<=result.w1){
			for(StringOperator2d::local_size_t i2=1; i2<= result.w2; i2++)
				if(result(d1,i2)!=StringOperator2d::spin_t()){
					flag = false;
					break;
				}
			if(flag)
				d1++;
		}
	}
	StringOperator2d::local_size_t d2=1;
	if(ls2==0 && rs2==0) {
		//left trim
		bool flag = true;
		while(flag && d2<=result.w2){
			for(StringOperator2d::local_size_t i1=1; i1<= result.w1; i1++)
				if(result(i1,d2)!=StringOperator2d::spin_t()){
					flag = false;
					break;
				}
			if(flag)
				d2++;
		}
	}
	StringOperator2d::local_size_t u1=result.w1;
	if(ls1+lhs.w1== rs1+rhs.w1) {
		;//right trim
		bool flag = true;
		while(flag && u1>=1){
			for(StringOperator2d::local_size_t i2=1; i2<= result.w2; i2++)
				if(result(u1,i2)!=StringOperator2d::spin_t()){
					flag = false;
					break;
				}
			if(flag)
				u1--;
		}
	}
	StringOperator2d::local_size_t u2=result.w2;
	if(ls2+lhs.w2== rs2+rhs.w2) {
		;//right trim
		bool flag = true;
		while(flag && u2>=1){
			for(StringOperator2d::local_size_t i1=1; i1<= result.w1; i1++)
				if(result(i1,u2)!=StringOperator2d::spin_t()){
					flag = false;
					break;
				}
			if(flag)
				u2--;
		}
	}
	if(d1!=1 || d2!=1 || u1!=result.w1 || u2!=result.w2){
		StringOperator2d result2;
		if(d1<=u1 && d2<=u2){
			result2 = StringOperator2d(u1-d1+1, u2-d2+1);
			for(StringOperator2d::local_size_t i1=1; i1<=result2.w1; i1++)
			for(StringOperator2d::local_size_t i2=1; i2<=result2.w2; i2++) {
				result2(i1,i2) = result(i1+d1-1, i2+d2-1);
			}
		}
		result = std::move(result2);
	}
	return make_pair(std::move(koef),std::move(result));
}

polynom<StringOperator2d::koef_t,StringOperator2d>
operator*(const StringOperator2d & lhs, const StringOperator2d & rhs) { // relevant only for commutator
	if(lhs==StringOperator2d())
		return polynom<StringOperator2d::koef_t,StringOperator2d>(StringOperator2d::koef_t(1),rhs);
	if(rhs==StringOperator2d())
		return polynom<StringOperator2d::koef_t,StringOperator2d>(StringOperator2d::koef_t(1),lhs);

	vector<pair<StringOperator2d::local_size_t,StringOperator2d::local_size_t>> s1;//ls1,rs1
	if(lhs.w1 > std::numeric_limits<StringOperator2d::local_size_t>::max() - rhs.w1)
		throw "size overflow 1";
	s1.reserve(lhs.w1+rhs.w1);
	s1.push_back(make_pair(0,0));
	for(StringOperator2d::local_size_t i=1; i<=rhs.w1-1; i++)
		s1.push_back(make_pair(i,0));
	for(StringOperator2d::local_size_t i=1; i<=lhs.w1-1; i++)
		s1.push_back(make_pair(0,i));

	vector<pair<StringOperator2d::local_size_t,StringOperator2d::local_size_t>> s2;//ls1,rs1
	if(lhs.w2 > std::numeric_limits<StringOperator2d::local_size_t>::max() - rhs.w2)
		throw "size overflow 2";
	s2.reserve(lhs.w2+rhs.w2);
	s2.push_back(make_pair(0,0));
	for(StringOperator2d::local_size_t i=1; i<=rhs.w2-1; i++)
		s2.push_back(make_pair(i,0));
	for(StringOperator2d::local_size_t i=1; i<=lhs.w2-1; i++)
		s2.push_back(make_pair(0,i));

	if ((lhs.w1+rhs.w1) != 0 && (lhs.w2+rhs.w2) > std::numeric_limits<StringOperator2d::local_size_t>::max() / (lhs.w1+rhs.w1))
		throw "size overflow 1*2";

	polynom<StringOperator2d::koef_t,StringOperator2d> result;
	for(auto p1 : s1)
	for(auto p2 : s2) {
		auto tmp = pairwaise_mul(lhs,p1.first,p2.first , rhs,p1.second,p2.second);
		result+=std::move(tmp.first)*std::move(tmp.second);
	}
	return std::move(result);
}
template<typename TB>
polynom<polynom<StringOperator2d::koef_t,TB>,StringOperator2d> 
operator*(polynom<StringOperator2d::koef_t,TB> && p, polynom<StringOperator2d::koef_t,StringOperator2d> && v){
	polynom<polynom<StringOperator2d::koef_t,TB>,StringOperator2d> result;
	for(auto vvvk : v)
		result[vvvk.first] = p*vvvk.second;
	return std::move(result);
}




/*
todo
сложные типы V
	в новом файле 2d 
		сначала умножение переменных возвращает полином
		потом   умножение переменных возвращает итератор
многопоточность
*/

polynom<complex<mpz_class>,cigma> operator*(complex<mpz_class> && k, cigma v){
	return polynom<complex<mpz_class>,cigma>(k,v);
}

int main() {
	{
		test_complex();
	}
	{
		cigma q;
		cout<<q<<" size="<<sizeof(q)<<endl;
		for(cigma l : {c1,cx,cy,cz})
			for(cigma r : {c1,cx,cy,cz})
				cout<<l<<" * "<<r<<" = "<<(l*r)    <<" ; ["<<l<<" , "<<r<<"] = "<<commute(1_re*l , 1_re*r)<<endl;
		cout << endl;
		cout << polynom(4*Xin(2)+3*Xin(5),cx) <<endl;
		cout << polynom(3*Xin(5),cx) <<endl;
		auto ini = std::tuple(2,3,cx);
		StringOperator2d op = {{cx,1,2},{cy,1,1}};
		cout<<op(1,2)<<" "<<op<<" "<<StringOperator2d()<<endl;
	}
	{
		auto q = polynom(4_re*Xin(2)+3_i*Xin(5),cx);
		cout << q<<"  ^2= "<<q*q<<endl;;
		complex<mpz_class> z{1};
	}
}