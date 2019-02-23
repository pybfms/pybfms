/****************************************************************************
 * ${bfm}_api.svh
 ****************************************************************************/
import ${bfm}_api_pkg::*;

`ifdef HAVE_HDL_VIRTUAL_INTERFACE
	${bfm}_api					m_api;
`else
	int unsigned				m_id;
	
	import "DPI-C" context function ${bfm}_register(string path);
	
	initial begin
		m_id = ${bfm}_register($sformat("%m");
	end
`endif

`ifdef HAVE_HDL_VIRTUAL_INTERFACE
${bfm_sv_vif_api}
`else
${bfm_sv_dpi_api}
`endif

