package main

import "os"
import "bufio"
import "strconv"
import "io"


func panic_on(err error) {
	if err!=nil { panic(err) }
}

func main() {
	const EOL = '\n'
	const HEAD_LEN = 4
	const OUT_CNT = 2
	
	var OUT [OUT_CNT]*os.File 
	var PR [OUT_CNT]*io.PipeReader
	var PW [OUT_CNT]*io.PipeWriter
	IN := bufio.NewReader(os.Stdin)
	
	// OPEN OUTPUT
	for i:=0;i<OUT_CNT;i++ {
		part := strconv.Itoa(i)
		f,err := os.Create("test/out"+part+".txt")
		OUT[i] = f
		panic_on(err)
		defer f.Close()
		// PIPES
		r,w := io.Pipe()
		PR[i] = r
		PW[i] = w
		defer r.Close()
		defer w.Close()
		go func(i int) {
			data := make([]byte,4096)
			for {
				n,err := PR[i].Read(data)
				if n==0 { return }
				panic_on(err)
				OUT[i].Write(data[:n])
			}
		}(i)
	}
	
	// MAIN LOOP
	mainLoop:
	for {
		for i:=0;i<OUT_CNT;i++ {
			// HEAD
			head := make([]byte,HEAD_LEN)
			n,err := IN.Read(head)
			if n==0 { break mainLoop }
			panic_on(err)
			// TAIL
			tail,err := IN.ReadBytes(EOL)
			panic_on(err)
			// OUTPUT TO PIPE
			PW[i].Write(head[:n])
			PW[i].Write(tail)
		}
	}
}
