import React, { useState, useEffect, useRef } from 'react';
import {
    Box, Typography, Container, Paper, Button,
    Divider, Grid, Toolbar, Alert, Snackbar, CircularProgress,
    IconButton, Tooltip, Breadcrumbs, Link, MenuItem, Select, FormControl, InputLabel, TextField, Dialog, DialogTitle, DialogContent, DialogActions, Chip, Stack, ToggleButtonGroup, ToggleButton
} from '@mui/material';
import {
    Save as SaveIcon,
    NavigateNext as NextIcon,
    FormatBold as BoldIcon,
    FormatItalic as ItalicIcon,
    FormatUnderlined as UnderlineIcon,
    FormatAlignLeft as LeftIcon,
    FormatAlignCenter as CenterIcon,
    FormatAlignRight as RightIcon,
    Image as ImageIcon,
    Add as AddIcon,
    Delete as DeleteIcon
} from '@mui/icons-material';
import Sidebar from '../components/Sidebar';
import { getTemplate, saveTemplate, getTemplateTypes } from '../services/api';

const TemplateEditor = () => {
    const [templateHtml, setTemplateHtml] = useState('');
    const [selectedType, setSelectedType] = useState('outpass');
    const [templateTypes, setTemplateTypes] = useState(['outpass', 'bonafide', 'leave']);
    const [variables, setVariables] = useState(['student_name', 'reason', 'date_from', 'date_to']);

    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [showSuccess, setShowSuccess] = useState(false);

    const [newTypeModal, setNewTypeModal] = useState(false);
    const [newTypeName, setNewTypeName] = useState('');
    const [newVarName, setNewVarName] = useState('');

    const templatePresets = [
        {
            name: "Classic Institutional",
            content: `
                <div style="text-align: center; font-family: 'Times New Roman', serif; border: 4px double #1e40af; padding: 40px;">
                    <h1 style="margin: 0; color: #1e40af; font-size: 32px;">UNIVERSITY OF EXCELLENCE</h1>
                    <p style="margin: 5px 0; font-weight: bold;">OFFICIAL OUTPASS AND LEAVE AUTHORIZATION</p>
                    <hr style="border: 1px solid #1e40af; margin: 20px 0;" />
                    <div style="text-align: left; font-size: 18px; line-height: 2;">
                        This is to certify that <strong>{student_name}</strong> is permitted to leave the campus premises for the following reason:<br/>
                        <strong>Purpose:</strong> {reason}<br/>
                        <strong>Departure:</strong> {date_from}<br/>
                        <strong>Reporting:</strong> {date_to}
                    </div>
                    <div style="margin-top: 60px; display: flex; justify-content: space-between;">
                        <p>___________________<br/>Student Signature</p>
                        <p>___________________<br/>Registrar / Warden</p>
                    </div>
                </div>
            `
        },
        {
            name: "Modern Professional",
            content: `
                <div style="font-family: 'Inter', sans-serif; color: #1e293b; padding: 20px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #3b82f6; padding-bottom: 20px; margin-bottom: 30px;">
                        <div>
                            <h1 style="margin: 0; font-size: 24px; color: #2563eb;">CAMPUS CONNECT</h1>
                            <p style="margin: 0; font-size: 12px; opacity: 0.7;">Digital Authorization System</p>
                        </div>
                        <div style="text-align: right;">
                            <p style="margin: 0; font-weight: 700;">OUTPASS CERTIFICATE</p>
                            <p style="margin: 0; font-size: 12px;">Valid upon Verification</p>
                        </div>
                    </div>
                    <p style="font-size: 16px; margin-bottom: 20px;">The administration hereby authorizes <strong>{student_name}</strong> to be off-campus for <strong>{reason}</strong>.</p>
                    <div style="background: #f8fafc; padding: 20px; border-radius: 12px; border: 1px solid #e2e8f0; margin-bottom: 30px;">
                        <div style="display: flex; margin-bottom: 10px;"><span style="width: 120px; font-weight: 600;">FROM:</span> <span>{date_from}</span></div>
                        <div style="display: flex;"><span style="width: 120px; font-weight: 600;">UNTIL:</span> <span>{date_to}</span></div>
                    </div>
                    <div style="text-align: center; margin-top: 50px;">
                        <div style="font-size: 10px; color: #64748b; margin-top: 20px;">Electronically signed by the System Administrator</div>
                    </div>
                </div>
            `
        }
    ];

    const applyPreset = (content) => {
        if (editorRef.current) {
            editorRef.current.innerHTML = content;
            setTemplateHtml(content);
        }
    };

    const editorRef = useRef(null);

    useEffect(() => {
        fetchTypes();
    }, []);

    useEffect(() => {
        fetchTemplate();
    }, [selectedType, fetchTemplate]);

    const fetchTypes = async () => {
        try {
            const res = await getTemplateTypes();
            setTemplateTypes(res.data);
        } catch (err) {
            console.error(err);
        }
    };

    useEffect(() => {
        if (!loading && editorRef.current) {
            editorRef.current.innerHTML = templateHtml;
        }
    }, [loading, templateHtml]); // Only sync when loading flips to false

    const fetchTemplate = async () => {
        setLoading(true);
        try {
            const res = await getTemplate(selectedType);
            setTemplateHtml(res.data.content);
            setVariables(res.data.variables || []);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleSave = async () => {
        setSaving(true);
        try {
            const content = editorRef.current.innerHTML;
            await saveTemplate(content, selectedType, variables);
            setShowSuccess(true);
            fetchTypes();
        } catch (err) {
            console.error(err);
        } finally {
            setSaving(false);
        }
    };

    const execCommand = (cmd, val = null) => {
        document.execCommand(cmd, false, val);
        editorRef.current.focus();
    };

    const handleImageUpload = (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (event) => {
                const imgStr = `<img src="${event.target.result}" style="max-width: 250px; display: block; margin: 20px auto;" />`;
                execCommand('insertHTML', imgStr);
            };
            reader.readAsDataURL(file);
        }
    };

    const insertVariable = (v) => {
        const span = `<span style="background-color: #f1f5f9; border: 1px solid #e2e8f0; padding: 2px 6px; border-radius: 4px; font-weight: 700; color: #3b82f6;">{${v}}</span>`;
        execCommand('insertHTML', span);
    };

    const addVariable = () => {
        if (newVarName && !variables.includes(newVarName)) {
            setVariables([...variables, newVarName]);
            setNewVarName('');
        }
    };

    const removeVariable = (v) => {
        setVariables(variables.filter(item => item !== v));
    };

    const handleCreateNewType = () => {
        if (newTypeName) {
            const sanitized = newTypeName.toLowerCase().replace(/\s+/g, '_');
            if (!templateTypes.includes(sanitized)) {
                setTemplateTypes([...templateTypes, sanitized]);
                setSelectedType(sanitized);
                setTemplateHtml(`<p>New template for ${newTypeName}</p>`);
                setVariables(['student_name', 'reason']); // Default minimal
                if (editorRef.current) editorRef.current.innerHTML = `<p>New template for ${newTypeName}</p>`;
            }
            setNewTypeModal(false);
            setNewTypeName('');
        }
    };

    return (
        <Box sx={{ display: 'flex', minHeight: '100vh', bgcolor: '#f1f5f9' }}>
            <Sidebar />

            <Box component="main" sx={{ flexGrow: 1, p: 4, width: { sm: `calc(100% - 260px)` } }}>
                <Toolbar />

                <Container maxWidth="xl">
                    <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <Box>
                            <Breadcrumbs separator={<NextIcon fontSize="small" />} sx={{ mb: 1 }}>
                                <Link underline="hover" color="inherit" href="/dashboard">Portal</Link>
                                <Typography color="text.primary">Design Studio</Typography>
                            </Breadcrumbs>
                            <Typography variant="h4" sx={{ fontWeight: 900, color: '#0f172a' }}>Document Studio</Typography>
                        </Box>

                        <Stack direction="row" spacing={2}>
                            <FormControl size="small" sx={{ width: 220 }}>
                                <InputLabel>Editing Template</InputLabel>
                                <Select
                                    value={selectedType}
                                    label="Editing Template"
                                    onChange={(e) => setSelectedType(e.target.value)}
                                    sx={{ bgcolor: 'white', fontWeight: 600 }}
                                >
                                    {templateTypes.map(t => (
                                        <MenuItem key={t} value={t}>{t.toUpperCase().replace('_', ' ')}</MenuItem>
                                    ))}
                                </Select>
                            </FormControl>
                            <Button variant="outlined" startIcon={<AddIcon />} onClick={() => setNewTypeModal(true)}>
                                Create New
                            </Button>
                            <Button
                                variant="contained"
                                startIcon={saving ? <CircularProgress size={20} color="inherit" /> : <SaveIcon />}
                                onClick={handleSave}
                                disabled={saving}
                                sx={{ px: 4, borderRadius: 2, fontWeight: 700, backgroundImage: 'linear-gradient(45deg, #2563eb, #3b82f6)' }}
                            >
                                Publish Design
                            </Button>
                        </Stack>
                    </Box>

                    <Grid container spacing={3}>
                        {/* Variable Management Sidebar */}
                        <Grid item xs={12} lg={3}>
                            <Paper sx={{ p: 3, borderRadius: 3, border: '1px solid #e2e8f0' }}>
                                <Typography variant="subtitle1" sx={{ fontWeight: 800, mb: 2 }}>DATA VARIABLES</Typography>
                                <Typography variant="caption" sx={{ color: 'text.secondary', display: 'block', mb: 2 }}>
                                    These fields will be collected by the chatbot from the student.
                                </Typography>

                                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 3 }}>
                                    {variables.map(v => (
                                        <Chip
                                            key={v}
                                            label={v}
                                            size="small"
                                            onDelete={() => removeVariable(v)}
                                            onClick={() => insertVariable(v)}
                                            sx={{ fontWeight: 600, bgcolor: '#eff6ff', color: '#1d4ed8', '&:hover': { bgcolor: '#dbeafe' } }}
                                            title="Click to insert at cursor"
                                        />
                                    ))}
                                </Box>

                                <Divider sx={{ mb: 2 }} />

                                <Typography variant="caption" sx={{ fontWeight: 700, mb: 1, display: 'block' }}>Add Custom Variable</Typography>
                                <Box sx={{ display: 'flex', gap: 1 }}>
                                    <TextField
                                        fullWidth
                                        size="small"
                                        placeholder="e.g. roll_no"
                                        value={newVarName}
                                        onChange={(e) => setNewVarName(e.target.value.toLowerCase().replace(/\s+/g, '_'))}
                                    />
                                    <IconButton color="primary" onClick={addVariable} disabled={!newVarName}>
                                        <AddIcon />
                                    </IconButton>
                                </Box>

                                <Divider sx={{ my: 3 }} />
                                <Typography variant="subtitle1" sx={{ fontWeight: 800, mb: 2 }}>DESIGN PRESETS</Typography>
                                <Stack spacing={1}>
                                    {templatePresets.map(preset => (
                                        <Button
                                            key={preset.name}
                                            variant="outlined"
                                            size="small"
                                            onClick={() => applyPreset(preset.content)}
                                            sx={{ textTransform: 'none', justifyContent: 'flex-start', borderRadius: 2 }}
                                        >
                                            {preset.name}
                                        </Button>
                                    ))}
                                </Stack>

                                <Box sx={{ mt: 4, p: 2, bgcolor: '#fff7ed', borderRadius: 2, border: '1px solid #fed7aa' }}>
                                    <Typography variant="caption" sx={{ color: '#9a3412', fontWeight: 700 }}>WORD TO THE WISE</Typography>
                                    <Typography variant="caption" sx={{ color: '#c2410c', display: 'block', mt: 0.5 }}>
                                        Variables you add here will be dynamically requested by the AI chatbot when a student asks for this document.
                                    </Typography>
                                </Box>
                            </Paper>
                        </Grid>

                        {/* Visual Toolbar & Editor */}
                        <Grid item xs={12} lg={9}>
                            <Paper
                                elevation={0}
                                sx={{
                                    p: 1,
                                    mb: 2,
                                    display: 'flex',
                                    gap: 1,
                                    alignItems: 'center',
                                    flexWrap: 'wrap',
                                    border: '1px solid #e2e8f0',
                                    borderRadius: 3,
                                    position: 'sticky',
                                    top: 80,
                                    zIndex: 10,
                                    bgcolor: 'rgba(255, 255, 255, 0.9)',
                                    backdropFilter: 'blur(8px)'
                                }}
                            >
                                <ToggleButtonGroup size="small">
                                    <ToggleButton value="bold" onClick={() => execCommand('bold')}><BoldIcon fontSize="small" /></ToggleButton>
                                    <ToggleButton value="italic" onClick={() => execCommand('italic')}><ItalicIcon fontSize="small" /></ToggleButton>
                                    <ToggleButton value="underline" onClick={() => execCommand('underline')}><UnderlineIcon fontSize="small" /></ToggleButton>
                                </ToggleButtonGroup>
                                <Divider orientation="vertical" flexItem />
                                <ToggleButtonGroup size="small">
                                    <ToggleButton value="left" onClick={() => execCommand('justifyLeft')}><LeftIcon fontSize="small" /></ToggleButton>
                                    <ToggleButton value="center" onClick={() => execCommand('justifyCenter')}><CenterIcon fontSize="small" /></ToggleButton>
                                    <ToggleButton value="right" onClick={() => execCommand('justifyRight')}><RightIcon fontSize="small" /></ToggleButton>
                                </ToggleButtonGroup>
                                <Divider orientation="vertical" flexItem />
                                <IconButton component="label">
                                    <ImageIcon fontSize="small" />
                                    <input type="file" hidden accept="image/*" onChange={handleImageUpload} />
                                </IconButton>
                                <Box sx={{ ml: 'auto', mr: 1 }}>
                                    <Typography variant="caption" sx={{ fontWeight: 700, color: 'text.secondary' }}>CANVAS: A4 PORTRAIT</Typography>
                                </Box>
                            </Paper>

                            <Box sx={{ display: 'flex', justifyContent: 'center' }}>
                                <Paper
                                    elevation={15}
                                    sx={{
                                        width: '100%',
                                        maxWidth: '850px',
                                        minHeight: '1100px',
                                        p: '80px',
                                        bgcolor: 'white',
                                        borderRadius: 1,
                                        border: '1px solid #e2e8f0',
                                        mb: 10,
                                        boxShadow: '0 25px 50px -12px rgb(0 0 0 / 0.15)'
                                    }}
                                >
                                    {loading ? (
                                        <Box display="flex" justifyContent="center" py={20}><CircularProgress /></Box>
                                    ) : (
                                        <div
                                            ref={editorRef}
                                            contentEditable
                                            suppressContentEditableWarning
                                            style={{
                                                outline: 'none',
                                                fontSize: '1.25rem',
                                                fontFamily: "'Times New Roman', serif",
                                                lineHeight: 1.8,
                                                minHeight: '900px',
                                                color: '#1e293b'
                                            }}
                                        />
                                    )}
                                </Paper>
                            </Box>
                        </Grid>
                    </Grid>
                </Container>
            </Box>

            {/* Create New Type Modal */}
            <Dialog open={newTypeModal} onClose={() => setNewTypeModal(false)}>
                <DialogTitle sx={{ fontWeight: 800 }}>Create New Institutional Document</DialogTitle>
                <DialogContent>
                    <Typography variant="body2" sx={{ mb: 2, color: 'text.secondary' }}>
                        Define a new type of certificate or authorization. This will create a fresh canvas for you to design.
                    </Typography>
                    <TextField
                        autoFocus
                        fullWidth
                        label="Document Name (e.g. Conduct Certificate)"
                        variant="outlined"
                        value={newTypeName}
                        onChange={(e) => setNewTypeName(e.target.value)}
                        sx={{ mt: 1 }}
                    />
                </DialogContent>
                <DialogActions sx={{ p: 3 }}>
                    <Button onClick={() => setNewTypeModal(false)}>Cancel</Button>
                    <Button variant="contained" onClick={handleCreateNewType} disabled={!newTypeName}>Initialize Design</Button>
                </DialogActions>
            </Dialog>

            <Snackbar open={showSuccess} autoHideDuration={4000} onClose={() => setShowSuccess(false)}>
                <Alert severity="success" variant="filled" sx={{ width: '100%' }}>
                    Document Design Published Successfully!
                </Alert>
            </Snackbar>
        </Box>
    );
};

export default TemplateEditor;
