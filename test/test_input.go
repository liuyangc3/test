package test

import (
	"fmt"
	"github.com/mozilla-services/heka/pipeline"
)

type TestInputConfig struct {
	Address  string `toml:"address"`
	ListName string `toml:"key"`
	DataBase string `toml:"db"`
}

type TestInput struct {
	conf *TestInputConfig
}

func (test *TestInput) ConfigStruct() interface{} {
	return &TestInputConfig{"localhost:6379", "heka", 0}
}

func (test *TestInput) Init(config interface{}) error {
	test.conf = config.(*TestInputConfig)
	fmt.Println(test.conf.Address, test.conf.ListName, test.conf.DataBase)
	return nil
}

func (test *TestInput) Run(ir pipeline.InputRunner, h pipeline.PluginHelper) error {
	for pack := range ir.InChan() {
		pack.Recycle(nil)
	}
	return nil
}

func init() {
	pipeline.RegisterPlugin("TestInput", func() interface{} {
		return new(TestInput)
	})
}
