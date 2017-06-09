package main

import "time"
// import "strings"
// TODO 
// asdasd
const (
	aa = iota
	bb
	cc
	dd
	ee
	zz_len
)

func main() {
	_ = `
		to
		jest\t
		test\t
		`
	N := 10000000
	t0 := time.Now()
	di := make(map[string]string,8)
	li := make([]string,100)
	di["a"] = "aaa"
	di["b"] = "bbb"
	di["c"] = "ccc"
	li[aa] = "aaa"
	li[bb] = "bbb"
	li[cc] = "ccc"
	for i:=0; i<N; i++ {
		//_ = di["a"]
		//_ = di["b"]
		//_ = di["c"]
		//_ = li[aa]
		//_ = li[bb]
		//_ = li[cc]
		
		_,_ = di["zzz"] // 259
		//for j:=0; j<20; j++ { // 20:300  100:800
		//	if li[j]=="zzz" { break }
		//}
		//_ = strings.Contains(":aaa:bbb:ccc:ddd:eee:ff:fgg:hhh:jjj:kkk:rrr:eee:rrr:ggg:hhh:jjj:uuu:ttt:rrr:eee:www:qqq:aaa:sss:ddd:",":"+"zzz"+":") // 660
		
	}
	println(int(float64(N)/time.Now().Sub(t0).Seconds()/1000),"Kops per sec")
}
