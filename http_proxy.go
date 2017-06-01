package main

import (
	"net"
	"fmt"
	"strings"
	"net/url"
	"bytes"
	"io"
)

func handleConnect (client net.Conn) {

	defer client.Close()

	var b [1024*10]byte
	n, err := client.Read(b[:])
	if err != nil {
		return
	}
	var methon, host, addr string
	fmt.Println(string(b[:n]))
	getData := string(b[:bytes.IndexByte(b[:], '\n')])
	fmt.Println(getData)
	fmt.Sscanf(getData, "%s %s", &methon, &host)
	fmt.Println(methon, host)
	u, err := url.Parse(host)
	fmt.Println(u)
	if err != nil {
		return
	}
	//http代理https流量
	if u.Opaque == "443" {
		addr = u.Scheme + ":" + u.Opaque
	} else {
		if u.Host != "" {
			if strings.Index(u.Host, ":") == -1 {
				addr = u.Host + ":80"
			} else {
				addr = u.Host
			}
		} else {
			addr = u.Path
		}
	}
	//连接远程服务器
	s, err := net.Dial("tcp", addr)
	fmt.Println("链接远程服务器")
	if err != nil {
		return
	}
	if methon == "CONNECT" {
		client.Write([]byte("HTTP/1.1 200 Connection established\r\nConnection: close\r\n\r\n"))
	} else {
		fmt.Println(string(b[:n]))
		s.Write(b[:n])
	}
	fmt.Println("写入数据")
	go io.Copy(s, client)
	io.Copy(client, s)



}

func main() {
	s, err := net.Listen("tcp", "0.0.0.0:11113")

	if err != nil {
		fmt.Println(err)
	}
	defer s.Close()
	for {
		conn, err := s.Accept()
		go handleConnect(conn)
		if err != nil {
			fmt.Println(err)
		}


	}

}
