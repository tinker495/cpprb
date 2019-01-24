#include <iostream>

#include <SegmentTree.hh>

int main(){

  auto st = ymd::SegmentTree<double>(16,[](auto a,auto b){ return a + b; });

  for(auto i = 0ul; i < 16ul; ++i){
    st.set(i,i*1.0);
    std::cout << i * 1.0 << " ";
  }
  std::cout << std::endl;

  std::cout << "[0,11): " << st.reduce(0,11) << std::endl;
  std::cout << "[13,15): " << st.reduce(13,15) << std::endl;

  std::cout << "[0,x) <= 7: x = "
	    << st.largest_region_index([](auto v){ return v <=7; })
	    << std::endl;

  st.set(12,5,10);
  for(auto i = 0ul; i < 16ul; ++i){
    std::cout << st.get(i) << " ";
  }
  std::cout << std::endl;

  std::cout << "[0,11): " << st.reduce(0,11) << std::endl;
  std::cout << "[13,15): " << st.reduce(13,15) << std::endl;

  std::cout << "[0,x) <= 7: x = "
	    << st.largest_region_index([](auto v){ return v <=7; })
	    << std::endl;

  return 0;
}
