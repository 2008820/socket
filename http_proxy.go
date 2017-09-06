package main

import (
	l "github.com/Sirupsen/logrus"
	"net"
	"fmt"
	"strings"
	"net/url"
	"bytes"
	"io"
	"os"
	"time"
)

const (
	serverIp = "0.0.0.0:11113"
)

func handleConnect(client net.Conn) {

	defer client.Close()
	err := client.SetDeadline(time.Now().Add(time.Duration(120) * time.Second))
	if err!=nil{
		l.Error(err)
	}
	var b [1024 * 10]byte
	n, err := client.Read(b[:])
	if err != nil {
		return
	}
	var methon, host, addr string
	var fristOne, body string
	getData := string(b[:bytes.IndexByte(b[:], '\n')])
	fmt.Sscanf(getData, "%s %s", &methon, &host)
	fmt.Sscanf(getData, "%s\r\n%s", &fristOne, &body)
	//fmt.Println(host)
	l.Info(host)
	u, err := url.Parse(host)
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
	if err != nil {
		return
	}
	errs := s.SetDeadline(time.Now().Add(time.Duration(120) * time.Second))
	if errs != nil {
		l.Error(errs)
	}
	defer s.Close()


	if methon == "CONNECT" {
		client.Write([]byte("HTTP/1.1 200 Connection established\r\nConnection: close\r\n\r\n"))
	} else {
		//fmt.Println(string(b[:n]))
		s.Write(b[:n])
	}

	go func() {
		defer s.Close()
		defer client.Close()
		io.Copy(s, client)
	}()

	io.Copy(client, s)
	l.Info("传输完成")



}

func main() {
	s, err := net.Listen("tcp", serverIp)
	pathStr := "proxy_log"
	dir ,_ := os.Getwd()
	fmt.Println(dir)
	_ = os.MkdirAll(pathStr, 0755)
	pathStr = fmt.Sprintf("%s/%s/proxy", dir, pathStr)
	fmt.Println(pathStr)
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
