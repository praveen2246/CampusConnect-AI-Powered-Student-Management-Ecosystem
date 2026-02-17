import React, { forwardRef } from 'react';
import { Box, Typography, Divider } from '@mui/material';

const OutpassPDF = forwardRef(({ outpass, template }, ref) => {
    if (!outpass) return null;

    const renderContent = () => {
        if (!template) return (
            <>
                <Typography variant="body1" sx={{ fontSize: '1.2rem', lineHeight: 2, mb: 4 }}>
                    This is to certify that <strong>{outpass.student_name}</strong>, a bona-fide student of this institution,
                    has been granted permission for leave as per the details provided below:
                </Typography>

                <Box sx={{ bgcolor: '#f8f9fa', p: 3, border: '1px solid #dee2e6', borderRadius: 1, mb: 4 }}>
                    <Box display="flex" sx={{ mb: 2 }}>
                        <Typography sx={{ width: '150px', fontWeight: 'bold' }}>Reason for Leave:</Typography>
                        <Typography>{outpass.reason}</Typography>
                    </Box>
                    <Box display="flex" sx={{ mb: 2 }}>
                        <Typography sx={{ width: '150px', fontWeight: 'bold' }}>Departure Date:</Typography>
                        <Typography>{outpass.date_from}</Typography>
                    </Box>
                    <Box display="flex" sx={{ mb: 2 }}>
                        <Typography sx={{ width: '150px', fontWeight: 'bold' }}>Expected Return:</Typography>
                        <Typography>{outpass.date_to}</Typography>
                    </Box>
                </Box>
            </>
        );

        let content = template
            .replace(/{student_name}/g, outpass.student_name)
            .replace(/{reason}/g, outpass.reason)
            .replace(/{date_from}/g, outpass.date_from)
            .replace(/{date_to}/g, outpass.date_to);

        return (
            <div
                className="template-content"
                dangerouslySetInnerHTML={{ __html: content }}
                style={{ fontSize: '1.25rem', lineHeight: 1.8, color: '#0f172a' }}
            />
        );
    };

    return (
        <div style={{ display: 'none' }}>
            <Box
                ref={ref}
                sx={{
                    p: 8,
                    width: '794px',
                    minHeight: '1123px',
                    bgcolor: 'white',
                    color: 'black',
                    fontFamily: "'Times New Roman', serif",
                    border: '1px solid #eee',
                    margin: 'auto',
                    position: 'relative',
                }}
            >
                {/* Institutional Header */}
                <Box sx={{ textAlign: 'center', mb: 6, pb: 4, borderBottom: '2px solid #1e293b' }}>
                    <Typography variant="h4" sx={{ fontWeight: 900, textTransform: 'uppercase', mb: 1, color: '#1e293b' }}>
                        College Connect - Admin Portal
                    </Typography>
                    <Typography variant="h6" sx={{ textTransform: 'uppercase', color: '#64748b', letterSpacing: 1 }}>
                        OFFICIAL LEAVE AUTHORIZATION
                    </Typography>
                </Box>

                {/* Meta Info */}
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 6 }}>
                    <Box>
                        <Typography variant="body2"><strong>REF NO:</strong> OP-{outpass._id?.slice(-8).toUpperCase()}</Typography>
                        <Typography variant="body2"><strong>ISSUED TO:</strong> {outpass.student_id}</Typography>
                    </Box>
                    <Box sx={{ textAlign: 'right' }}>
                        <Typography variant="body2"><strong>DATE:</strong> {new Date().toLocaleDateString()}</Typography>
                    </Box>
                </Box>

                {/* Main Content */}
                <Box sx={{ minHeight: '500px' }}>
                    {renderContent()}
                </Box>

                {/* Signatures */}
                <Box sx={{ mt: 'auto', display: 'flex', justifyContent: 'space-between', pt: 10 }}>
                    <Box sx={{ textAlign: 'center' }}>
                        <Box sx={{ borderBottom: '1px solid black', width: '150px', mb: 1 }}></Box>
                        <Typography variant="caption" sx={{ fontWeight: 700 }}>STUDENT SIGNATURE</Typography>
                    </Box>
                    <Box sx={{ textAlign: 'center' }}>
                        <Typography sx={{ color: 'primary.main', fontWeight: 900, fontStyle: 'italic', mb: 0.5 }}>DIGITALLY VERIFIED</Typography>
                        <Box sx={{ borderBottom: '1px solid black', width: '150px', mb: 1 }}></Box>
                        <Typography variant="caption" sx={{ fontWeight: 700 }}>AUTHORIZED REGISTRAR</Typography>
                    </Box>
                </Box>

                <Box sx={{ position: 'absolute', bottom: 40, left: 0, right: 0, textAlign: 'center' }}>
                    <Typography variant="caption" color="text.secondary">
                        This is a computer-generated document. Verification can be done via the Admin Portal.
                    </Typography>
                </Box>
            </Box>
        </div>
    );
});

export default OutpassPDF;
