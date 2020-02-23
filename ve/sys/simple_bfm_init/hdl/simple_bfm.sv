
module simple_bfm #(parameter P=0)(
	input		clk
	);

    task hdl_task(int unsigned val);
        $display("hdl_task: %0d", val);
        py_task(val+1);
    endtask
    
    task init();
    	set_parameters(P);
    endtask

${pybfms_api_impl}

endmodule
