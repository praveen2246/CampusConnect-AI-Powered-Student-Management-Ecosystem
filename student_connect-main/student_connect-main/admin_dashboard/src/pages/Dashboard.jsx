import React, { useEffect, useState, useRef } from 'react';
import {
    Box, Typography, Container, Table, TableBody, TableCell,
    TableHead, TableRow, Paper, Chip, Button, IconButton,
    Tooltip, Toolbar, Skeleton, Fade
} from '@mui/material';
import {
    Download as DownloadIcon,
    Refresh as RefreshIcon,
    Visibility as ViewIcon,
    CheckCircle as ApproveIcon,
    Cancel as RejectIcon
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useReactToPrint } from 'react-to-print';
import { getOutpasses, updateOutpassStatus, getTemplate } from '../services/api';
import Sidebar from '../components/Sidebar';
import OutpassPDF from '../components/OutpassPDF';
import { motion } from 'framer-motion';

const Dashboard = () => {
    const [outpasses, setOutpasses] = useState([]);
    const [template, setTemplate] = useState('');
    const [loading, setLoading] = useState(true);
    const [selectedOutpass, setSelectedOutpass] = useState(null);
    const navigate = useNavigate();
    const componentRef = useRef();

    useEffect(() => {
        fetchOutpasses();
        fetchTemplate();
    }, []);

    const fetchTemplate = async () => {
        try {
            const res = await getTemplate();
            setTemplate(res.data.content);
        } catch (err) {
            console.error(err);
        }
    };

    const fetchOutpasses = async () => {
        setLoading(true);
        try {
            const res = await getOutpasses();
            setOutpasses(res.data);
        } catch (err) {
            if (err.response?.status === 401) navigate('/');
        } finally {
            setTimeout(() => setLoading(false), 500);
        }
    };

    const handleAction = async (id, status) => {
        try {
            await updateOutpassStatus(id, status);
            fetchOutpasses();
        } catch (err) {
            console.error(err);
        }
    };

    // const handlePrint = useReactToPrint({
    //     content: () => componentRef.current,
    //     documentTitle: `Outpass_${selectedOutpass?.student_name}`,
    // });

    const downloadPDF = (outpass) => {
        // Use the official backend download link which has the variables attached
        const url = `http://localhost:8000/outpass/download/${outpass._id}`;
        window.open(url, '_blank');
    };

    const getStatusChip = (status) => {
        const configs = {
            'APPROVED': { color: 'success', label: 'Authorized' },
            'REJECTED': { color: 'error', label: 'Declined' },
            'PENDING': { color: 'warning', label: 'Review Pending' }
        };
        const config = configs[status] || { color: 'default', label: status };
        return (
            <Chip
                label={config.label}
                color={config.color}
                size="small"
                sx={{ fontWeight: 600, px: 1 }}
            />
        );
    };

    return (
        <Box sx={{ display: 'flex', minHeight: '100vh', bgcolor: 'background.default' }}>
            <Sidebar />

            <Box component="main" sx={{ flexGrow: 1, p: 4, width: { sm: `calc(100% - 260px)` } }}>
                <Toolbar /> {/* Spacer */}

                <Fade in={true}>
                    <Container maxWidth="xl">
                        {/* Header Section */}
                        <Box display="flex" justifyContent="space-between" alignItems="center" mb={4}>
                            <Box>
                                <Typography variant="h4" gutterBottom>
                                    Certificate Management
                                </Typography>
                                <Typography variant="body2" color="text.secondary">
                                    Track and manage student leave authorizations efficiently.
                                </Typography>
                            </Box>
                            <Button
                                variant="outlined"
                                startIcon={<RefreshIcon />}
                                onClick={fetchOutpasses}
                                sx={{ borderRadius: 2 }}
                            >
                                Sync Data
                            </Button>
                        </Box>

                        {/* Stats Summary (Minimalist) */}
                        <Box display="grid" gridTemplateColumns="repeat(auto-fit, minmax(200px, 1fr))" gap={3} mb={4}>
                            {[
                                { label: 'Active Requests', value: outpasses.filter(o => o.status === 'PENDING').length, color: 'orange' },
                                { label: 'Issued Today', value: outpasses.filter(o => o.status === 'APPROVED').length, color: '#2563eb' },
                            ].map((stat, i) => (
                                <Paper key={i} sx={{ p: 2, borderLeft: `4px solid ${stat.color}` }}>
                                    <Typography variant="caption" color="text.secondary" sx={{ textTransform: 'uppercase', fontWeight: 600 }}>
                                        {stat.label}
                                    </Typography>
                                    <Typography variant="h5" sx={{ fontWeight: 700 }}>{stat.value}</Typography>
                                </Paper>
                            ))}
                        </Box>

                        {/* Table Section */}
                        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
                            <Paper sx={{ width: '100%', overflow: 'hidden', borderRadius: 2 }}>
                                <Table>
                                    <TableHead sx={{ bgcolor: '#f1f5f9' }}>
                                        <TableRow>
                                            <TableCell sx={{ fontWeight: 700 }}>Type</TableCell>
                                            <TableCell sx={{ fontWeight: 700 }}>Student Detail</TableCell>
                                            <TableCell sx={{ fontWeight: 700 }}>Reason</TableCell>
                                            <TableCell sx={{ fontWeight: 700 }}>Duration</TableCell>
                                            <TableCell sx={{ fontWeight: 700 }}>Current Status</TableCell>
                                            <TableCell sx={{ fontWeight: 700 }} align="right">System Actions</TableCell>
                                        </TableRow>
                                    </TableHead>
                                    <TableBody>
                                        {loading ? (
                                            [...Array(5)].map((_, i) => (
                                                <TableRow key={i}>
                                                    <TableCell colSpan={5}><Skeleton height={50} /></TableCell>
                                                </TableRow>
                                            ))
                                        ) : outpasses.length === 0 ? (
                                            <TableRow>
                                                <TableCell colSpan={5} align="center" sx={{ py: 10 }}>
                                                    <Typography color="text.secondary">No requests found in the system.</Typography>
                                                </TableCell>
                                            </TableRow>
                                        ) : (
                                            outpasses.map((row) => (
                                                <TableRow key={row._id} hover>
                                                    <TableCell>
                                                        <Chip
                                                            label={(row.type || 'outpass').toUpperCase()}
                                                            size="small"
                                                            variant="outlined"
                                                            sx={{ fontWeight: 700, borderRadius: 1 }}
                                                        />
                                                    </TableCell>
                                                    <TableCell>
                                                        <Typography variant="body2" sx={{ fontWeight: 600 }}>{row.student_name || 'Anonymous Student'}</Typography>
                                                        <Typography variant="caption" color="text.secondary">ID: {row.student_id?.slice(-8)}</Typography>
                                                    </TableCell>
                                                    <TableCell>
                                                        <Typography variant="body2">{row.reason}</Typography>
                                                    </TableCell>
                                                    <TableCell>
                                                        <Box>
                                                            <Typography variant="caption" display="block"><b>From:</b> {row.date_from}</Typography>
                                                            <Typography variant="caption" display="block"><b>To:</b> {row.date_to}</Typography>
                                                        </Box>
                                                    </TableCell>
                                                    <TableCell>
                                                        {getStatusChip(row.status)}
                                                    </TableCell>
                                                    <TableCell align="right">
                                                        <Box display="flex" justifyContent="flex-end" gap={1} alignItems="center">
                                                            {row.status === 'PENDING' && (
                                                                <>
                                                                    <Tooltip title="Approve">
                                                                        <IconButton color="success" onClick={() => handleAction(row._id, 'APPROVED')}>
                                                                            <ApproveIcon />
                                                                        </IconButton>
                                                                    </Tooltip>
                                                                    <Tooltip title="Reject">
                                                                        <IconButton color="error" onClick={() => handleAction(row._id, 'REJECTED')}>
                                                                            <RejectIcon />
                                                                        </IconButton>
                                                                    </Tooltip>
                                                                </>
                                                            )}
                                                            {row.status === 'APPROVED' && (
                                                                <Button
                                                                    variant="contained"
                                                                    size="small"
                                                                    startIcon={<DownloadIcon />}
                                                                    onClick={() => downloadPDF(row)}
                                                                    sx={{
                                                                        borderRadius: 2,
                                                                        boxShadow: '0 4px 6px -1px rgb(37 99 235 / 0.2)',
                                                                        textTransform: 'none',
                                                                        fontWeight: 700
                                                                    }}
                                                                >
                                                                    Download Certificate
                                                                </Button>
                                                            )}
                                                        </Box>
                                                    </TableCell>
                                                </TableRow>
                                            ))
                                        )}
                                    </TableBody>
                                </Table>
                            </Paper>
                        </motion.div>
                    </Container>
                </Fade>
            </Box>

            {/* Hidden printable component */}
            <OutpassPDF ref={componentRef} outpass={selectedOutpass} template={template} />
        </Box>
    );
};

export default Dashboard;
