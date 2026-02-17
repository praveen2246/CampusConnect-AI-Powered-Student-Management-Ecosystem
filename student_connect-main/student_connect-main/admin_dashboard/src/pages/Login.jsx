import React, { useState } from 'react';
import {
    TextField, Button, Box, Typography, Paper, Alert,
    InputAdornment, IconButton, Container
} from '@mui/material';
import {
    Visibility, VisibilityOff,
    LockOutlined as LockIcon,
    EmailOutlined as EmailIcon
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { loginAdmin } from '../services/api';
import { motion } from 'framer-motion';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        try {
            const response = await loginAdmin({ email, password });
            localStorage.setItem('adminToken', response.data.token);
            navigate('/dashboard');
        } catch {
            setError('The credentials provided are incorrect. Access denied.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <Box
            sx={{
                minHeight: '100vh',
                width: '100vw',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center',
                background: 'linear-gradient(135deg, #1e293b 0%, #0f172a 100%)',
                margin: 0,
                padding: 0,
                overflowX: 'hidden'
            }}
        >
            <Container maxWidth="sm">
                <motion.div
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ duration: 0.5 }}
                >
                    <Paper
                        elevation={24}
                        sx={{
                            p: { xs: 4, md: 6 },
                            borderRadius: 4,
                            textAlign: 'center',
                            bgcolor: 'rgba(255, 255, 255, 0.98)',
                            backdropFilter: 'blur(10px)'
                        }}
                    >
                        <Box sx={{ mb: 4, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 2 }}>
                            <Box
                                sx={{
                                    width: 50,
                                    height: 50,
                                    bgcolor: 'primary.main',
                                    borderRadius: 2,
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    color: 'white',
                                    fontWeight: 'bold',
                                    fontSize: '1.5rem'
                                }}
                            >
                                A
                            </Box>
                            <Typography variant="h4" sx={{ fontWeight: 900, color: '#0f172a', letterSpacing: -1 }}>
                                ADMIN DASHBOARD
                            </Typography>
                        </Box>

                        <Typography variant="h5" sx={{ fontWeight: 800, mb: 1, color: '#1e293b' }}>
                            Institutional Control
                        </Typography>
                        <Typography variant="body2" sx={{ color: 'text.secondary', mb: 4 }}>
                            Authorize and manage administrative workflows.
                        </Typography>

                        {error && (
                            <Alert severity="error" sx={{ mb: 3, textAlign: 'left', borderRadius: 2 }}>
                                {error}
                            </Alert>
                        )}

                        <form onSubmit={handleLogin}>
                            <TextField
                                fullWidth
                                label="Admin Email"
                                margin="normal"
                                variant="outlined"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                InputProps={{
                                    startAdornment: (
                                        <InputAdornment position="start">
                                            <EmailIcon size="small" />
                                        </InputAdornment>
                                    ),
                                }}
                                sx={{ mb: 2 }}
                            />
                            <TextField
                                fullWidth
                                label="Access Key"
                                type={showPassword ? 'text' : 'password'}
                                margin="normal"
                                variant="outlined"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                InputProps={{
                                    startAdornment: (
                                        <InputAdornment position="start">
                                            <LockIcon size="small" />
                                        </InputAdornment>
                                    ),
                                    endAdornment: (
                                        <InputAdornment position="end">
                                            <IconButton onClick={() => setShowPassword(!showPassword)} edge="end">
                                                {showPassword ? <VisibilityOff /> : <Visibility />}
                                            </IconButton>
                                        </InputAdornment>
                                    )
                                }}
                                sx={{ mb: 3 }}
                            />
                            <Button
                                fullWidth
                                variant="contained"
                                size="large"
                                type="submit"
                                disabled={loading}
                                sx={{
                                    py: 1.8,
                                    fontSize: '1.2rem',
                                    fontWeight: 800,
                                    borderRadius: 3,
                                    boxShadow: '0 4px 6px -1px rgb(37 99 235 / 0.4)',
                                    backgroundImage: 'linear-gradient(45deg, #2563eb, #7c3aed)',
                                    '&:hover': {
                                        boxShadow: '0 10px 15px -3px rgb(37 99 235 / 0.5)',
                                    }
                                }}
                            >
                                {loading ? 'ACCESSING...' : 'LOGIN TO ADMIN'}
                            </Button>
                        </form>
                    </Paper>
                </motion.div>
            </Container>
        </Box>
    );
};

export default Login;
