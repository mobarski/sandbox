package main

import "os"
import "bufio"
import "fmt"


func panic_on(err error) {
	if err!=nil { panic(err) }
}

func main() {
	const EOL = '\n'
	const HEAD_LEN = 100
	const OUT_CNT = 2
	var OUT [OUT_CNT]os.File
	
	for i:=0;i<OUT_CNT;i++ {
		OUT[i],err := os.Create("out"+string(i)+".txt")
		panic_on(err)
	}
	
	fmt.Println(">>>")
	head := make([]byte,HEAD_LEN)
	ri := bufio.NewReader(os.Stdin)
	n,err := ri.Read(head)
	panic_on(err)
	if n==0 { } // TODO
	tail,err := ri.ReadBytes(EOL)
	panic_on(err)
	os.Stdout.Write(head[:n])
	os.Stdout.Write(tail)
}
