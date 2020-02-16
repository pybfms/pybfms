
module simple_bfm(
	input		clk
	);

    task hdl_task(int unsigned val);
        $display("hdl_task: %0d", val);
        py_task(val+1);
    endtask

${pybfms_api_impl}

endmodule
